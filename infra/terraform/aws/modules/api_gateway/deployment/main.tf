resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = var.api_gateway_id
  stage_name  = "dev"
}