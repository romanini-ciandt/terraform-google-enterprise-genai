/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

module "env" {
  source = "../../modules/base_env"

  env                          = "development"
  business_code                = "bu3"
  business_unit                = "business_unit_3"
  remote_state_bucket          = var.remote_state_bucket
  location_kms                 = var.location_kms
  location_gcs                 = var.location_gcs
  tfc_org_name                 = var.tfc_org_name
  peering_module_depends_on    = var.peering_module_depends_on
  peering_iap_fw_rules_enabled = true
  subnet_region                = var.instance_region
  subnet_ip_range              = "10.5.64.0/21"
}

module "ml_env" {
  source = "../../modules/ml_env"

  env                  = "development"
  business_code        = "bu3"
  business_unit        = "business_unit_3"
  remote_state_bucket  = var.remote_state_bucket
  location_gcs         = var.location_gcs
  tfc_org_name         = var.tfc_org_name
  business_unit_folder = module.env.business_unit_folder

  depends_on = [module.env]
}