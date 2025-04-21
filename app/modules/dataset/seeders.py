import os
import shutil
import json
from app.modules.auth.models import User
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from core.seeders.BaseSeeder import BaseSeeder
from app.modules.dataset.models import (
    DataSet,
    DSMetaData,
    PublicationType,
    DSMetrics,
    Author)
from datetime import datetime, timezone
from dotenv import load_dotenv


class DataSetSeeder(BaseSeeder):

    priority = 2  # Lower priority

    def run(self):

        fixed_dates = [
            datetime(2021, 1, 15, 10, 0, tzinfo=timezone.utc),
            datetime(2021, 6, 20, 14, 30, tzinfo=timezone.utc),
            datetime(2022, 3, 10, 8, 15, tzinfo=timezone.utc),
            datetime(2023, 8, 5, 18, 45, tzinfo=timezone.utc)
        ]

        fixed_sizes = [1024, 2048, 5120, 8192, 10240, 20480, 51200, 102400, 204800, 409600, 1024000, 2048000]

        # Retrieve users
        user1 = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user2@example.com').first()

        if not user1 or not user2:
            raise ValueError("Users not found. Please seed users first.")

        # Create DSMetrics instances
        ds_metrics_list = [
            DSMetrics(number_of_models=5, number_of_features=10),
            DSMetrics(number_of_models=50, number_of_features=20),
            DSMetrics(number_of_models=100, number_of_features=30),
            DSMetrics(number_of_models=75, number_of_features=40)
        ]
        seeded_ds_metrics = self.seed(ds_metrics_list)

        # Create DSMetaData instances
        ds_meta_data_list = [
            DSMetaData(
                deposition_id=1 + i,
                title=f'Sample dataset {i + 1}',
                description=f'Description for dataset {i + 1}',
                publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
                publication_doi=f'10.1234/dataset{i + 1}',
                dataset_doi=f'10.1234/dataset{i + 1}',
                tags='tag1, tag2',
                ds_metrics_id=seeded_ds_metrics[i].id
            ) for i in range(4)
        ]

        # Change the title of the last dataset to adapt it to explore command tests in discord bot
        ds_meta_data_list[3].title = 'Test dataset for discord bot'
        ds_meta_data_list[3].description = 'Test dataset for testing explore command in discord bot.'
        seeded_ds_meta_data = self.seed(ds_meta_data_list)

        # Create Author instances and associate with DSMetaData
        ds_authors = [
            Author(
                name=f'DS Author {i + 1}',
                affiliation=f'Affiliation {i + 1}',
                orcid=f'0000-0000-0000-000{i}',
                ds_meta_data_id=seeded_ds_meta_data[i].id
            ) for i in range(4)
        ]
        self.seed(ds_authors)

        # Create DataSet instances with fixed dates
        datasets = [
            DataSet(
                user_id=user1.id if i % 2 == 0 else user2.id,
                ds_meta_data_id=seeded_ds_meta_data[i].id,
                created_at=fixed_dates[i]
            ) for i in range(4)
        ]
        seeded_datasets = self.seed(datasets)

        # Create FMMetaData instances
        fm_meta_data_list = [
            FMMetaData(
                uvl_filename=f'file{i + 1}.uvl',
                title=f'Feature Model {i + 1}',
                description=f'Description for feature model {i + 1}',
                publication_type=PublicationType.SOFTWARE_DOCUMENTATION,
                publication_doi=f'10.1234/fm{i + 1}',
                tags='tag1, tag2',
                uvl_version='1.0'
            ) for i in range(12)
        ]
        seeded_fm_meta_data = self.seed(fm_meta_data_list)

        # Create Author instances and associate with FMMetaData
        fm_authors = [
            Author(
                name=f'FM Author {i + 1}',
                affiliation=f'Affiliation {i + 1}',
                orcid=f'0000-0000-0000-100{i}',
                fm_meta_data_id=seeded_fm_meta_data[i].id
            ) for i in range(12)
        ]
        self.seed(fm_authors)

        # Create FeatureModel instances
        feature_models = [
            FeatureModel(
                data_set_id=seeded_datasets[i // 3].id,
                fm_meta_data_id=seeded_fm_meta_data[i].id
            ) for i in range(12)
        ]
        seeded_feature_models = self.seed(feature_models)

        # Create files with structured JSON content and fixed sizes
        load_dotenv()
        working_dir = os.getenv('WORKING_DIR', '')
        src_folder = os.path.join(working_dir, 'app', 'modules', 'dataset', 'uvl_examples')
        for i in range(12):
            file_name = f'file{i + 1}.uvl'
            feature_model = seeded_feature_models[i]
            dataset = next(ds for ds in seeded_datasets if ds.id == feature_model.data_set_id)
            user_id = dataset.user_id

            dest_folder = os.path.join(working_dir, 'uploads', f'user_{user_id}', f'dataset_{dataset.id}')
            os.makedirs(dest_folder, exist_ok=True)

            # Create structured JSON content
            uvl_content = {
                "feature_model": {
                    "id": feature_model.id,
                    "title": f"Feature Model {i + 1}",
                    "description": f"Description for feature model {i + 1}",
                    "dataset_id": dataset.id,
                    "user_id": user_id,
                    "tags": ["tag1", "tag2"],
                    "uvl_version": "1.0"
                }
            }

            # Write JSON content to the file
            json_file_path = os.path.join(src_folder, file_name)
            with open(json_file_path, 'w') as f:
                json.dump(uvl_content, f, indent=4)

            # Add padding to match the fixed size
            fixed_size = fixed_sizes[i % len(fixed_sizes)]
            with open(json_file_path, 'ab') as f:
                current_size = f.tell()
                if current_size < fixed_size:
                    padding = fixed_size - current_size
                    f.write(b' ' * padding)  # Add spaces as padding

            # Copy the file to the destination
            shutil.copy(json_file_path, dest_folder)

            uvl_file = Hubfile(
                name=file_name,
                checksum=f'checksum{i + 1}',
                size=fixed_size,
                feature_model_id=feature_model.id
            )
            self.seed([uvl_file])
