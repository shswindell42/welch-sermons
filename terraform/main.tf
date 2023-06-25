# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.60.0"
    }
  }

  required_version = ">= 1.1.0"
}

variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}
variable "subscription_id" {
  
}

provider "azurerm" {
  features {
  }

  subscription_id = var.subscription_id

  client_id = var.client_id
  client_secret = var.client_secret
  tenant_id = var.tenant_id
}


resource "azurerm_resource_group" "welch-sermons" {
    location = "eastus"
    name = "welch-sermons"
}

resource "azurerm_cognitive_account" "ocr-service" {
    location = "EastUS"
    name = "welch-sermon-ocr"
    resource_group_name = azurerm_resource_group.welch-sermons.name

    kind = "ComputerVision"
    sku_name = "F0"

    custom_subdomain_name = "welch-sermon-ocr"
    dynamic_throttling_enabled = false

    network_acls {
      default_action = "Deny"
      ip_rules = [
        "67.177.191.78"
      ]
    }
}

