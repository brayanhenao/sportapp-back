provider "aws" {
  region = "us-east-1"
}

data "aws_secretsmanager_secret" "db_credentials" {
  name = "DB_CREDENTIALS"
}

data "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = data.aws_secretsmanager_secret.db_credentials.id
}

# Network configuration

module "vpc" {
  source   = "../modules/vpc/vpc"
  vpc_name = "sportapp-vpc"
  vpc_cidr = "10.0.0.0/16"
}

module "subnet_1" {
  source            = "../modules/vpc/subnet"
  vpc_id            = module.vpc.id
  subnet_name       = "sportapp-subnet-1"
  subnet_cidr_block = cidrsubnet(module.vpc.cidr_block, 8, 1)
  availability_zone = "us-east-1a"
  depends_on        = [module.vpc]
}

module "subnet_2" {
  source            = "../modules/vpc/subnet"
  vpc_id            = module.vpc.id
  subnet_name       = "sportapp-subnet-2"
  subnet_cidr_block = cidrsubnet(module.vpc.cidr_block, 8, 2)
  availability_zone = "us-east-1b"
  depends_on        = [module.vpc]
}

module "subnet_3" {
  source            = "../modules/vpc/subnet"
  vpc_id            = module.vpc.id
  subnet_name       = "sportapp-subnet-3"
  subnet_cidr_block = cidrsubnet(module.vpc.cidr_block, 8, 3)
  availability_zone = "us-east-1c"
  depends_on        = [module.vpc]
}

# Database configuration

module "db" {
  source        = "../modules/rds"
  database_name = "sportapp"
  username      = jsondecode(sensitive(data.aws_secretsmanager_secret_version.db_credentials.secret_string)).username
  password      = jsondecode(sensitive(data.aws_secretsmanager_secret_version.db_credentials.secret_string)).password
  subnet_ids    = [module.subnet_1.id, module.subnet_2.id, module.subnet_3.id]

  depends_on = [module.subnet_1, module.subnet_2, module.subnet_3]
}

resource "aws_secretsmanager_secret_version" "db_credentials_version" {
  secret_id     = data.aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = jsondecode(sensitive(data.aws_secretsmanager_secret_version.db_credentials.secret_string)).username
    password = jsondecode(sensitive(data.aws_secretsmanager_secret_version.db_credentials.secret_string)).password
    port     = jsondecode(sensitive(data.aws_secretsmanager_secret_version.db_credentials.secret_string)).port
    host     = module.db.host
    name     = jsondecode(sensitive(data.aws_secretsmanager_secret_version.db_credentials.secret_string)).name
  })

  depends_on = [module.db]
}

# Load balancer configuration

module "application_load_balancer" {
  source  = "../modules/elb/alb"
  name    = "sportapp-alb"
  subnets = [module.subnet_1.id, module.subnet_2.id, module.subnet_3.id]

  depends_on = [module.vpc, module.subnet_1, module.subnet_2, module.subnet_3]
}

module "application_load_balancer_listener" {
  source            = "../modules/elb/listener"
  listener_port     = 8000
  listener_protocol = "HTTP"
  load_balancer_arn = module.application_load_balancer.arn

  depends_on = [module.application_load_balancer]
}

# API Gateway configuration

module "api_gateway" {
  source          = "../modules/api_gateway/api"
  api_description = "Sportapp API Gateway"
  api_name        = "sportapp-gateway"
}

# API Gateway authorizer configuration

module "authorizer_role" {
  source = "../modules/api_gateway/authorizer_role"
}

module "api_gateway_free_plan_authorizer" {
  source = "../modules/api_gateway/authorizer"

  authorizer_name  = "FreePlanAuthorizer"
  authorizer_scope = "free"
  lambda_role_arn  = module.authorizer_role.role_arn
}

module "api_gateway_intermediate_plan_authorizer" {
  source = "../modules/api_gateway/authorizer"

  authorizer_name  = "IntermediatePlanAuthorizer"
  authorizer_scope = "intermediate"
  lambda_role_arn  = module.authorizer_role.role_arn
}

module "api_gateway_premium_plan_authorizer" {
  source = "../modules/api_gateway/authorizer"

  authorizer_name  = "PremiumPlanAuthorizer"
  authorizer_scope = "premium"
  lambda_role_arn  = module.authorizer_role.role_arn
}

module "api_gateway_business_partner_authorizer" {
  source = "../modules/api_gateway/authorizer"

  authorizer_name  = "BusinessPartnerAuthorizer"
  authorizer_scope = "business_partner"
  lambda_role_arn  = module.authorizer_role.role_arn
}

module "sports-get-all-route" {
  source                   = "../modules/api_gateway/route"
  api_id                   = module.api_gateway.gateway_id
  route_integration_method = "GET"
  route_integration_uri    = "https://webhook.site/472aeab7-db0a-4291-bd00-3675ae239c9b"
  route_method             = "GET"
  route_path               = "/bhenao"
  depends_on               = [module.api_gateway_free_plan_authorizer]
}

# ECS configuration

module "ecs_cluster" {
  source       = "../modules/ecs/cluster"
  cluster_name = "sportapp-cluster"

  depends_on = [module.vpc]
}

# SQS configuration

module "nutritional_queue" {
  source     = "../modules/sqs"
  queue_name = "nutritional_plan_queue.fifo"
}

module "adverse_incidents_queue" {
  source     = "../modules/sqs"
  queue_name = "adverse_incidents_queue.fifo"
}
