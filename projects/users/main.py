"""
Este archivo contiene los experimentos realizados para el escenario de calidad de escalabiliad del proyecto de grado: SportApp.
Los experimentos realizados son los siguientes:
E
xperimento 1: Registro en base de datos directo: Se realiza el registro de un usuario en una base de datos directamente y se escala horizontalmente.
Conclusión: Se necesitan 15 instancias del microservicio para soportar 1000 usuarios concurrentes además de una  base de datos con 560 conexiones máximas.
Experimento 1.1: Registro en base de datos directo con background tasks: Se realiza el registro de un usuario en una base de datos directamente posterior a la petición del cliente.
Conclusión: Los usuarios reciben una respuesta más rápida, pero las background tasks requieren igual cantidad de recursos que el experimento 1.

Experimento 2: Registro en memoria y sincronización vertical: Se realiza el registro de un usuario en memoria y se sincroniza con una base de datos principal.
A partir del Experimento 1 se identificó que el cuello de botella es la base de datos, por lo que se realizó un experimento para realizar el registro en bulk en la base de datos.
Esto genera un procesamiento asíncrono y una respuesta más rápida al cliente. sin embargo dado que el email es un campo único, se generan errores que deben ser reportados al cliente.
con lo cual se plantean 2 opciones de sincronización vertical y 2 opciones de sincronización de estado con el cliente.

Experimento 2: Sincronización vertical con base de datos local: Se realiza el registro en memoria y se sincroniza con una base de datos local sqlite.
Experimento 2: Sincronización vertical sin base de datos local: Se realiza el registro en memoria y se sincroniza con una base de datos principal.

Opciones de sincronizar estado con el cliente en Experimento 2:
Experimento 2.1 (Polling), Obtener el estado de un usuario por email mediante polling.
Experimento 2.2 (SSE), Obtener el estado de un usuario por email mediante Server Sent Events en la misma petición de registro.

Conclusión: El experimento 2.2 es el más eficiente en términos de recursos, ya que no requiere de polling y el cliente recibe una respuesta en tiempo real.
No requiere escalar la base de datos y el microservicio soporta 1000 usuarios concurrentes con 5 instancias.
la sincronización vertical con base de datos local no es recomendada ya que requiere de recursos adicionales y no es tan eficiente como la sincronización vertical sin base de datos local.

"""

import asyncio
from os import environ as env
from typing import List, Dict

from fastapi import FastAPI, Depends, BackgroundTasks
from sse_starlette.sse import EventSourceResponse
from starlette.responses import JSONResponse

from utils import AWSClient
from models import User, UserCreate
from db import SessionLocal, engine, Base

app = FastAPI()


# get_db es inyectado por fastapi para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


# Experimentos:

# Experimento 1 registro en base de datos directo
@app.post("/user")
async def create_user(user: UserCreate, db=Depends(get_db)):
    user = User(name=user.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Experimento 1.1 registro en base de datos directo con background tasks

def _create_user(db, user):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/user2")
async def create_user2(user: UserCreate, background_tasks: BackgroundTasks, db=Depends(get_db)):
    user = User(name=user.name)
    background_tasks.add_task(_create_user, db, user)
    return user


# Experimento 2 registro en memoria y sincronización vertical async(sin uso de base de datos local)
users: List[User] = []  # Lista de usuarios a ser sincronizados

users_with_errors_by_email_map: Dict[str, User] = {}  # Mapa de usuarios con errores por email (email repetido
users_success_by_email_map: Dict[str, User] = {}  # Mapa de usuarios con éxito por email


@app.post("/mock")
async def root(user: UserCreate, db=Depends(get_db)):
    global users
    user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    users.append(user)
    return {"message": user.__dict__}


# Experimento 2 Syncronización vertical (sin uso de base de datos local)
async def syncdb(aws_client):
    global users
    db = SessionLocal()
    total_users_by_run = int(env.get("TOTAL_USERS_BY_RUN", 50))  # Cognito limits
    while True:
        if users:
            process_users = users[0:total_users_by_run]

            repeated_users = db.query(User).filter(User.email.in_([user.email for user in process_users])).all()

            for i, user in enumerate(repeated_users):
                del process_users[i]
                users_with_errors_by_email_map[user.email] = user


            # Cognito no permite crear usuarios en bulk, por lo que se debe crear uno por uno y esto es muy costoso
            # operacionalmente además de que posee un límite de 50 usuarios por llamada. Decisión final: No usar Cognito
            # sino guardar la contraseña en la base de datos (hash). El login se realizará en este servicio y la autenticación
            # mediante un Lambda Authorizer.

            # for user in process_users:
            #     aws_client.cognito.create_user(
            #         user=user,
            #     )
            #
            #     aws_client.cognito.set_permanent_password(
            #         email=user.email,
            #         password=f'{user.first_name}A1234!'
            #     )

            db.bulk_save_objects(process_users)
            db.commit()
            users = users[total_users_by_run:]
            users_success_by_email_map.update({user.email: user for user in process_users})
        sync_every = int(env.get("SYNC_EVERY", 2))
        await asyncio.sleep(sync_every)
    db.close()


# Experimento 2 Syncronización vertical con base de datos local
async def vertical_sync_db(db, db_global):
    while True:
        local_users = db.query(User).all()
        if local_users:
            db.query(User).delete()
            db_global.bulk_save_objects(local_users)
            db.commit()
            db_global.commit()
        await asyncio.sleep(5)
    db.close()
    db_global.close()


# Experimento 2: Proceso asincrono de sincronización vertical
@app.on_event("startup")
async def startup():
    # Usar estas lineas para sincronización vertical con base de datos local

    # global_engine, SessionGlobal = _create_engine()
    # Base.metadata.create_all(bind=global_engine)
    Base.metadata.create_all(bind=engine)
    #
    # db_global = SessionGlobal()
    # db = SessionLocal()
    #
    # asyncio.create_task(vertical_sync_db(db, db_global)) # Sincronización vertical con base de datos local
    aws_client = AWSClient()
    asyncio.create_task(syncdb(aws_client))  # Sincronización vertical sin base de datos local


# Opciones de sincronizar estado con el cliente en Experimento 2

# Experimento 2.1 (Polling), Obtener el estado de un usuario por email, (No recomendado)
@app.get("/mock/{email}")
async def result(email: str):
    global users_with_errors_by_email_map
    global users_success_by_email_map
    if email in users_with_errors_by_email_map:
        del users_with_errors_by_email_map[email]
        return JSONResponse(status_code=400, content={"message": "User already exists"})
    elif email in users_success_by_email_map:
        del users_success_by_email_map[email]
        return JSONResponse(status_code=200, content={"message": "User created"})

    return JSONResponse(status_code=202, content={"message": "Pending"})


# Experimento 2.2 (SSE), Obtener el estado de un usuario por email mediante Server Sent Events
@app.post("/mock/stream")
async def mock_stream(user: UserCreate):
    global users
    user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    users.append(user)

    async def event_generator(user):
        global users_with_errors_by_email_map
        global users_success_by_email_map
        while True:
            if user.email in users_with_errors_by_email_map:
                del users_with_errors_by_email_map[user.email]
                yield f"User already exists\n\n"
                break
            elif user.email in users_success_by_email_map:
                del users_success_by_email_map[user.email]
                yield f"User created\n\n"
                break
            yield f"Pending\n\n"
            await asyncio.sleep(1)

    return EventSourceResponse(event_generator(user))
