from veryfi.client_base import Client


class Tags:
    def __init__(self, client: Client):
        self.client = client

    def get_tags(self, document_id):
        """
        Return all Tag assigned to a specific Document.
        https://docs.veryfi.com/api/receipts-invoices/get-document-tags/

        :param document_id: ID of the document you'd like to get
        :return: Added tags data
        """
        endpoint_name = f"/documents/{document_id}/tags"
        return self.client._request("GET", endpoint_name, {})

    def add_tag(self, document_id, tag_name):
        """
        Add a new tag on an existing document.
        https://docs.veryfi.com/api/receipts-invoices/add-a-tag-to-a-document/

        :param document_id: ID of the document you'd like to update
        :param tag_name: name of the new tag
        :return: Added tag data
        """
        endpoint_name = f"/documents/{document_id}/tags/"
        request_arguments = {"name": tag_name}
        return self.client._request("PUT", endpoint_name, request_arguments)

    def replace_tags(self, document_id, tags):
        """
        Replace multiple tags on an existing document.
        https://docs.veryfi.com/api/receipts-invoices/update-a-document/

        :param document_id: ID of the document you'd like to update
        :param tags: array of strings
        :return: Added tags data
        """
        endpoint_name = f"/documents/{document_id}/"
        request_arguments = {"tags": tags}
        return self.client._request("PUT", endpoint_name, request_arguments)

    def add_tags(self, document_id, tags):
        """
        Add multiple tags on an existing document.
        https://docs.veryfi.com/api/receipts-invoices/add-tags-to-a-document/

        :param document_id: ID of the document you'd like to update
        :param tags: array of strings
        :return: Added tags data
        """
        endpoint_name = f"/documents/{document_id}/tags/"
        request_arguments = {"tags": tags}
        return self.client._request("POST", endpoint_name, request_arguments)

    def delete_tag(self, document_id, tag_id):
        """
        Unlink a tag from the list of tags assigned to a specific Document.
        https://docs.veryfi.com/api/receipts-invoices/unlink-a-tag-from-a-document/

        :param document_id: ID of the document
        :param tag_id: ID of the tag you'd like to unlink
        """
        endpoint_name = f"/documents/{document_id}/tags/{tag_id}"
        self.client._request("DELETE", endpoint_name, {})

    def delete_tags(self, document_id):
        """
        Unlink all tags assigned to a specific Document.
        https://docs.veryfi.com/api/receipts-invoices/unlink-all-tags-from-a-document/

        :param document_id: ID of the document
        """
        endpoint_name = f"/documents/{document_id}/tags"
        self.client._request("DELETE", endpoint_name, {})
