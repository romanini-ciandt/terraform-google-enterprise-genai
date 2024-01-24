<!-- BEGIN_TF_DOCS -->
Copyright 2024 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [google_vertex_ai_tensorboard.tensorboard](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/vertex_ai_tensorboard) | resource |
| [google_kms_crypto_key.key](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/kms_crypto_key) | data source |
| [google_kms_key_ring.kms](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/kms_key_ring) | data source |
| [google_project.project](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/project) | data source |
| [google_projects.kms](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/projects) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_keyring_name"></a> [keyring\_name](#input\_keyring\_name) | Central keyring name | `string` | `"sample-keyring"` | no |
| <a name="input_name"></a> [name](#input\_name) | The name of the metadata store instance | `string` | `null` | no |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | Optional Project ID. | `string` | `null` | no |
| <a name="input_region"></a> [region](#input\_region) | The resource region, one of [us-central1, us-east4]. | `string` | `"us-central1"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_blob_storage_path_prefix"></a> [blob\_storage\_path\_prefix](#output\_blob\_storage\_path\_prefix) | Consumer project Cloud Storage path prefix used to store blob data, which can either be a bucket or directory. Does not end with a '/'. |
| <a name="output_id"></a> [id](#output\_id) | an identifier for the resource with format {{name}} |
| <a name="output_name"></a> [name](#output\_name) | Name of the Tensorboard. |
<!-- END_TF_DOCS -->