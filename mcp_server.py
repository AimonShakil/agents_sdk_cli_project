from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", stateless_http=True)

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
        name = "read_document",
        description = "Read a document from dict above"
)
async def read_docs(doc_id: str) -> str:
    return docs.get(doc_id, "Document not found")


# TODO: Write a tool to edit a doc
@mcp.tool(
    name= "edit_document",
    description = "Edit a document by replacing a string in a documents content with a new string"
)

def edit_document(
    doc_id: str = Field(description = "Id of the document that will be edited"),
    old_str: str = Field(description=" The Text to replace Must match exactly, including white space"),
    new_str: str= Field(description=" The New text to insert in place of the old text")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    
# TODO: Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type='application/json'
)

def list_doc() -> list[str]:
    return list (docs.keys()) # mcp python automatically convert whatever we return into a string for us

# TODO: Write a resource to return the contents of a particular doc
# mime types: text.json, text.pdf, appdlication.pdf , multipurpose internet mail extension
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id{doc_id} not found")
    return docs[doc_id]


# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name= "format",
    descriptions="Rewrites the contents of the documents in Markdown Format"
)
def format_document(
    doc_id: str = Field(description= "Id of the document to format"),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is: 
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullets, tables etc as necessary. Use the 'edit_document tool to edit the document"""

    return [
        base.UserMessage(prompt)
    ]

# TODO: Write a prompt to summarize a doc

mcp_server = mcp.streamable_http_app()





    