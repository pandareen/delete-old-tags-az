# Create a ContainerRegistryClient that will authenticate through Active Directory
from azure.containerregistry import ContainerRegistryClient
from azure.identity import DefaultAzureCredential
from azure.containerregistry import ArtifactTagOrder

import argparse


def main():
    # Parse the command line argument for the configuration file.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--acr-name",
        required=True,
        type=str,
        help="Specify the name of the Azure container registry",
    )
    parser.add_argument(
        "--repository-name",
        required=True,
        type=str,
        help="Specify the name of the container image",
    )
    parser.add_argument(
        "--latest-tag",
        required=True,
        type=str,
        help="Specify latest tag. Keep the latest tag and delete all other tags",
    )

    args = parser.parse_args()

    endpoint = f"https://{args.acr_name}.azurecr.io"

    with ContainerRegistryClient(endpoint, DefaultAzureCredential(), audience="https://management.azure.com") as client:

        print(f"found {client.list_repository_names()} repositories")
        tag_props = client.list_tag_properties(args.repository_name, order_by=ArtifactTagOrder.LAST_UPDATED_ON_DESCENDING)
        print(f"These are the list for container image {args.repository_name}")
        print(''.join([p.name + '\t' + str(p.last_updated_on) + '\n' for p in list(tag_props)]))

        for tag in client.list_tag_properties(args.repository_name, order_by=ArtifactTagOrder.LAST_UPDATED_ON_DESCENDING):
            if tag.name == args.latest_tag:
                print(f"skipping delete of {tag.name} because this is set as latest tag")
                continue
            print(f"found tag {tag.name}")
            print("Deleting {}:{}".format(args.repository_name, tag.name))
            client.delete_tag(args.repository_name, tag.name)


if __name__ == "__main__":
    main()
