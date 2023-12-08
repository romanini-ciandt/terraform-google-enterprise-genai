/**
 * Copyright 2021 Google LLC
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

output "base_shared_vpc_project" {
  description = "Project machine learning project."
  value       = module.machine_learning_project.project_id
}

output "access_context_manager_policy_id" {
  description = "Access Context Manager Policy ID."
  value       = local.access_context_manager_policy_id
}

output "bucket" {
  description = "The created storage bucket."
  value       = module.gcs_buckets.bucket
}
