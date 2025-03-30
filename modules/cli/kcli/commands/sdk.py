import os
import time
import typer
import string
import pathlib
from rich.progress import Progress, SpinnerColumn, TextColumn
import kcli.commands.templates as templates
import kcli.utils as utils
import typing
import datetime

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent

ROOT_DIR = string.Template(f"{BASE_DIR}/modules/connectors/$id")
SCHEMAS_DIR = string.Template(f"{BASE_DIR}/modules/connectors/$id/schemas")
TESTS_DIR = string.Template(f"{BASE_DIR}/modules/connectors/$id/tests/$id")
MAPPERS_DIR = string.Template(f"{BASE_DIR}/modules/connectors/$id/karrio/mappers/$id")
PROVIDERS_DIR = string.Template(
    f"{BASE_DIR}/modules/connectors/$id/karrio/providers/$id"
)
SCHEMA_DATATYPES_DIR = string.Template(
    f"{BASE_DIR}/modules/connectors/$id/karrio/schemas/$id"
)


def _add_extension(
    id: str,
    name: str,
    feature: str,
    version: str,
    is_xml_api: bool,
):
    typer.confirm(
        f'Generate new carrier: "{name}" extension with id "{id}" and features [{feature}]',
        abort=True,
    )

    features = [f.strip() for f in feature.split(",")]
    context = dict(
        id=id,
        name=name,
        features=features,
        version=version,
        is_xml_api=is_xml_api,
        compact_name=name.strip()
        .replace("-", "")
        .replace("_", "")
        .replace("&", "")
        .replace(" ", ""),
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        os.makedirs(TESTS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(SCHEMAS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(MAPPERS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(PROVIDERS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(SCHEMA_DATATYPES_DIR.substitute(id=id), exist_ok=True)
        time.sleep(1)

        # project files
        templates.SETUP_TEMPLATE.stream(**context).dump(
            f"{ROOT_DIR.substitute(id=id)}/setup.py"
        )
        templates.README_TEMPLATE.stream(**context).dump(
            f"{ROOT_DIR.substitute(id=id)}/README.md"
        )
        (
            templates.XML_GENERATE_TEMPLATE
            if is_xml_api
            else templates.JSON_GENERATE_TEMPLATE
        ).stream(**context).dump(f"{ROOT_DIR.substitute(id=id)}/generate")

        # schema files
        (
            templates.XML_SCHEMA_TEMPLATE
            if is_xml_api
            else templates.JSON_SCHEMA_TEMPLATE
        ).stream(**context).dump(
            f"{SCHEMAS_DIR.substitute(id=id)}/error_response.{'xsd' if is_xml_api else 'json'}"
        )
        templates.EMPTY_FILE_TEMPLATE.stream(**context).dump(
            f"{SCHEMA_DATATYPES_DIR.substitute(id=id)}/__init__.py"
        )

        # tests files
        templates.TEST_FIXTURE_TEMPLATE.stream(**context).dump(
            f"{TESTS_DIR.substitute(id=id)}/fixture.py"
        )
        templates.TEST_PROVIDER_IMPORTS_TEMPLATE.stream(**context).dump(
            f"{TESTS_DIR.substitute(id=id)}/__init__.py"
        )
        templates.TEST_IMPORTS_TEMPLATE.stream(**context).dump(
            f"{ROOT_DIR.substitute(id=id)}/tests/__init__.py"
        )

        # mappers files
        templates.MAPPER_TEMPLATE.stream(**context).dump(
            f"{MAPPERS_DIR.substitute(id=id)}/mapper.py"
        )
        templates.MAPPER_PROXY_TEMPLATE.stream(**context).dump(
            f"{MAPPERS_DIR.substitute(id=id)}/proxy.py"
        )
        templates.MAPPER_SETTINGS_TEMPLATE.stream(**context).dump(
            f"{MAPPERS_DIR.substitute(id=id)}/settings.py"
        )
        templates.MAPPER_METADATA_TEMPLATE.stream(**context).dump(
            f"{MAPPERS_DIR.substitute(id=id)}/__init__.py"
        )

        # providers files
        templates.PROVIDER_ERROR_TEMPLATE.stream(**context).dump(
            f"{PROVIDERS_DIR.substitute(id=id)}/error.py"
        )
        templates.PROVIDER_UNITS_TEMPLATE.stream(**context).dump(
            f"{PROVIDERS_DIR.substitute(id=id)}/units.py"
        )
        templates.PROVIDER_UTILS_TEMPLATE.stream(**context).dump(
            f"{PROVIDERS_DIR.substitute(id=id)}/utils.py"
        )
        templates.PROVIDER_IMPORTS_TEMPLATE.stream(**context).dump(
            f"{PROVIDERS_DIR.substitute(id=id)}/__init__.py"
        )

        if "address" in features:
            templates.TEST_ADDRESS_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_address.py"
            )

            templates.PROVIDER_ADDRESS_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/address.py"
            )

        if "rating" in features:
            templates.TEST_RATE_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_rate.py"
            )

            templates.PROVIDER_RATE_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/rate.py"
            )

        if "tracking" in features:
            templates.TEST_TRACKING_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_tracking.py"
            )

            templates.PROVIDER_TRACKING_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/tracking.py"
            )

        if "document" in features:
            templates.TEST_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_document.py"
            )

            templates.PROVIDER_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/document.py"
            )

        if "manifest" in features:
            templates.TEST_MANIFEST_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_manifest.py"
            )

            templates.PROVIDER_MANIFEST_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/manifest.py"
            )

        if "shipping" in features:
            templates.TEST_SHIPMENT_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_shipment.py"
            )

            os.makedirs(f"{PROVIDERS_DIR.substitute(id=id)}/shipment", exist_ok=True)
            templates.PROVIDER_SHIPMENT_CANCEL_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/shipment/cancel.py"
            )
            templates.PROVIDER_SHIPMENT_CREATE_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/shipment/create.py"
            )
            templates.PROVIDER_SHIPMENT_IMPORTS_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/shipment/__init__.py"
            )

        if "pickup" in features:
            templates.TEST_PICKUP_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_pickup.py"
            )

            os.makedirs(f"{PROVIDERS_DIR.substitute(id=id)}/pickup", exist_ok=True)
            templates.PROVIDER_PICKUP_CANCEL_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/pickup/cancel.py"
            )
            templates.PROVIDER_PICKUP_CREATE_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/pickup/create.py"
            )
            templates.PROVIDER_PICKUP_UPDATE_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/pickup/update.py"
            )
            templates.PROVIDER_PICKUP_IMPORTS_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/pickup/__init__.py"
            )

    typer.echo("Done!")


def _add_features(
    id: str,
    name: str,
    feature: str,
    is_xml_api: bool,
):
    typer.confirm(
        f'Bootstrap features for: "{name}" extension with id "{id}"',
        abort=True,
    )

    features = [f.strip() for f in feature.split(",")]
    context = dict(
        id=id,
        name=name,
        features=features,
        is_xml_api=is_xml_api,
        compact_name=name.strip()
        .replace("-", "")
        .replace("_", "")
        .replace("&", "")
        .replace(" ", ""),
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        os.makedirs(TESTS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(SCHEMAS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(MAPPERS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(PROVIDERS_DIR.substitute(id=id), exist_ok=True)
        os.makedirs(SCHEMA_DATATYPES_DIR.substitute(id=id), exist_ok=True)
        time.sleep(1)

        if "address" in features:
            templates.TEST_ADDRESS_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_address.py"
            )

            templates.PROVIDER_ADDRESS_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/address.py"
            )

        if "rating" in features:
            templates.TEST_RATE_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_rate.py"
            )

            templates.PROVIDER_RATE_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/rate.py"
            )

        if "tracking" in features:
            templates.TEST_TRACKING_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_tracking.py"
            )

            templates.PROVIDER_TRACKING_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/tracking.py"
            )

        if "document" in features:
            templates.TEST_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_document.py"
            )

            templates.PROVIDER_DOCUMENT_UPLOAD_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/document.py"
            )

        if "manifest" in features:
            templates.TEST_MANIFEST_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_manifest.py"
            )

            templates.PROVIDER_MANIFEST_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/manifest.py"
            )

        if "shipping" in features:
            templates.TEST_SHIPMENT_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_shipment.py"
            )

            os.makedirs(f"{PROVIDERS_DIR.substitute(id=id)}/shipment", exist_ok=True)
            templates.PROVIDER_SHIPMENT_CANCEL_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/shipment/cancel.py"
            )
            templates.PROVIDER_SHIPMENT_CREATE_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/shipment/create.py"
            )
            templates.PROVIDER_SHIPMENT_IMPORTS_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/shipment/__init__.py"
            )

        if "pickup" in features:
            templates.TEST_PICKUP_TEMPLATE.stream(**context).dump(
                f"{TESTS_DIR.substitute(id=id)}/test_pickup.py"
            )

            os.makedirs(f"{PROVIDERS_DIR.substitute(id=id)}/pickup", exist_ok=True)
            templates.PROVIDER_PICKUP_CANCEL_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/pickup/cancel.py"
            )
            templates.PROVIDER_PICKUP_CREATE_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/pickup/create.py"
            )
            templates.PROVIDER_PICKUP_UPDATE_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/pickup/update.py"
            )
            templates.PROVIDER_PICKUP_IMPORTS_TEMPLATE.stream(**context).dump(
                f"{PROVIDERS_DIR.substitute(id=id)}/pickup/__init__.py"
            )

    typer.echo("Done!")


app = typer.Typer()


@app.command()
def add_extension(
    carrier_slug: str = typer.Option(..., prompt=True),
    display_name: str = typer.Option(..., prompt=True),
    features: typing.Optional[str] = typer.Option(
        ", ".join(utils.DEFAULT_FEATURES), prompt=True
    ),
    version: typing.Optional[str] = typer.Option(
        f"{datetime.datetime.now().strftime('%Y.%-m')}", prompt=True
    ),
    is_xml_api: typing.Optional[bool] = typer.Option(False, prompt="Is XML API?"),
):
    typer.confirm(
        f'Generate new carrier: "{display_name}" extension with id "{carrier_slug}" and features [{features}]',
        abort=True,
    )

    _add_extension(
        carrier_slug.lower(),
        display_name,
        features,
        version,
        is_xml_api,
    )


@app.command()
def add_features(
    carrier_slug: str = typer.Option(..., prompt=True),
    display_name: str = typer.Option(..., prompt=True),
    features: typing.Optional[str] = typer.Option(
        ", ".join(utils.DEFAULT_FEATURES), prompt=True
    ),
    is_xml_api: typing.Optional[bool] = typer.Option(False, prompt="Is XML API?"),
):
    features = features.split(",")
    features = [feature.strip() for feature in features]
    _add_features(carrier_slug, display_name, ",".join(features), is_xml_api)
