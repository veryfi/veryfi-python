from typing import Dict

from veryfi.client_base import Client


class LineItems:
    def __init__(self, client: Client):
        self.client = client

    def get_line_items(self, document_id: int):
        """
        Retrieve all line items for a document.
        https://docs.veryfi.com/api/receipts-invoices/get-document-line-items/

        :param document_id: ID of the document you'd like to retrieve
        :return: List of line items extracted from the document
        """
        return self.client._request("GET", f"/documents/{document_id}/line-items/")

    def get_line_item(self, document_id: int, line_item_id: int):
        """
        Retrieve a line item for existing document by ID.
        https://docs.veryfi.com/api/receipts-invoices/get-a-line-item/

        :param document_id: ID of the document you'd like to retrieve
        :param line_item_id: ID of the line item you'd like to retrieve
        :return: Line item extracted from the document
        """
        return self.client._request("GET", f"/documents/{document_id}/line-items/{line_item_id}")

    def add_line_item(self, document_id: int, payload: Dict) -> Dict:
        """
        Add a new line item on an existing document.
        https://docs.veryfi.com/api/receipts-invoices/create-a-line-item/

        :param document_id: ID of the document you'd like to update
        :param payload: line item object to add
        :return: Added line item data
        """
        return self.client._request("POST", f"/documents/{document_id}/line-items/", payload)

    def update_line_item(self, document_id: int, line_item_id: int, payload: Dict) -> Dict:
        """
        Update an existing line item on an existing document.
        https://docs.veryfi.com/api/receipts-invoices/update-a-line-item/

        :param document_id: ID of the document you'd like to update
        :param line_item_id: ID of the line item you'd like to update
        :param payload: line item object to update
        :return: Line item data with updated fields, if fields are writable. Otherwise line item data with unchanged fields.
        """
        return self.client._request(
            "PUT", f"/documents/{document_id}/line-items/{line_item_id}", payload
        )

    def delete_line_items(self, document_id: int):
        """
        Delete all line items on an existing document.
        https://docs.veryfi.com/api/receipts-invoices/delete-all-document-line-items/

        :param document_id: ID of the document you'd like to delete
        """
        self.client._request("DELETE", f"/documents/{document_id}/line-items/")

    def delete_line_item(self, document_id: int, line_item_id: int):
        """
        Delete an existing line item on an existing document.
        https://docs.veryfi.com/api/receipts-invoices/delete-a-line-item/

        :param document_id: ID of the document you'd like to delete
        :param line_item_id: ID of the line item you'd like to delete
        """
        self.client._request("DELETE", f"/documents/{document_id}/line-items/{line_item_id}")
