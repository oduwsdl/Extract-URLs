import datetime
import json
import os

import flask
import requests


class APIUtil:
  """
  The ``APIUtil`` class is a collection of helper functions required to serve the HTTP API for Robust PDFLinks Service.
  It consist of default HTTP error response strings, and functions that generate error responses, cast payloads to JSON,
  extract query parameters, call the Robust Links API, handle LDP handshakes, and generate LDN payloads.

  """

  ERR_TITLE = "Error!"
  ERR_REQ_NOT_JSON = "Expected JSON payload"
  ERR_PDF_NOT_FOUND = "The requested PDF file was not found"
  ERR_PDF_META_NOT_FOUND = "The metadata for the requested PDF file was not found. Please try uploading the PDF again to generate metadata."
  ERR_MAPPING_NOT_FOUND = "This PDF does not have any saved URI-R > URI-M mappings"
  ERR_ONLY_PDF_ALLOWED = "You are only allowed to upload PDF files"
  ERR_MALFORMED_LDN = "The LDN is malformed"
  ERR_MISSING_PARAM_FILE = "Missing required parameter 'file'"
  ERR_MISSING_PARAM_LD_SERVER_URL = "Missing required parameter 'ld_server_url'"
  ERR_MISSING_PARAM_PDF_URL = "Missing required query parameter 'pdf_url'"
  ERR_MISSING_PARAM_MAPPING_URL = "Missing required query parameter 'mapping_url'"

  def __init__(self, app: flask.Flask):
    self.app = app

  @staticmethod
  def make_error_res(status: int, message: str):
    """
    Generate an error response.

    If the request accepts HTML, the error will be rendered as a HTML page.
    Instead, if the request accepts JSON, the error will be rendered as JSON.
    If neither, the error will be rendered as plain text.

    :param status: HTTP status code
    :param message: Message included in the error response
    :return: An HTTP response with the given status and message

    """

    mimes = flask.request.accept_mimetypes
    if mimes.accept_html:
      body = flask.render_template('error.html', title=APIUtil.ERR_TITLE, message=message)
    elif mimes.accept_json:
      body = {"ok": False, "timestamp": datetime.datetime.utcnow().isoformat(), "error": message}
    else:
      body = message
    return flask.make_response(body, status)

  def call_robust_links_svc(self, uri: str):
    """
    Call the Robust PDFLinks service on a URI, and return the status of its robustification.

    A success response has the following fields.

    * ``ok``: always True
    * ``uri``: The URL which was sent to the Robust PDFLinks service
    * ``href_uri_r``: Robust Link pointing to the original resource
    * ``href_uri_m``: Robust Link pointing to an archived copy of the original resource (i.e., memento)

    An error response has the following fields.

    * ``ok``: always False
    * ``uri``: The URL which was sent to the Robust PDFLinks service
    * ``error``: A friendly description of the error

    :param uri: the URL to robustify
    :return: the status of robustification

    """

    # log the function call
    self.app.logger.info(f"Submitted request to RL service for URL: {uri}")

    # send the request
    params = {"url": uri, "anchor_text": uri}
    headers = {"Accept": "application/json"}
    res = requests.get(f"http://robustlinks.mementoweb.org/api/", params=params, headers=headers)

    def error_res(__errmsg: str):
      self.app.logger.warning(__errmsg)
      return {"ok": False, "uri": uri, "error": __errmsg}

    def success_res(__rl: any, __uri_r_key='original_url_as_href', __uri_m_key='memento_url_as_href'):
      self.app.logger.info(f"RL service robustified URL: {uri}")
      return {"ok": True, "uri": uri, "href_uri_r": minify(__rl[__uri_r_key]), "href_uri_m": minify(__rl[__uri_m_key])}

    def minify(html: str):
      return html.replace('\n', '').strip()

    try:
      # try converting response to JSON
      res_json: dict = res.json()
    except json.JSONDecodeError:
      # if the response is not JSON
      return error_res(f"RL service returned HTTP {res.status_code} with a non JSON response for URI: {uri}")
    else:
      # if the response is JSON
      if 'robust_links_html' in res_json:
        # handle responses with 'robust_links_html'
        return success_res(res_json['robust_links_html'])
      elif 'friendly error' in res_json:
        # handle responses with 'friendly error'
        errmsg = res_json['friendly error'].strip()
        return error_res(f"RL service returned HTTP {res.status_code} for URI: {uri}. Message: {errmsg}")
      else:
        # handle responses that do not have the expected fields
        return error_res(f"RL service returned HTTP {res.status_code} with an unknown JSON response for URI: {uri}")

  def generate_ldn_payload(self, pdf_hash: str, ld_server_url: str, ldp_inbox_url: str):
    """
    Generate an LDN payload for a PDF, given the ``pdf_hash``, ``ld_server_url``, and ``ldp_inbox_url``.

    This function checks if the PDF exists and if not, returns a ``400 Bad Request`` HTTP response.
    Next, it checks if the PDF metadata exists and if not, returns a ``400 Bad Request`` HTTP response.
    Upon doing so, it gets the original PDF name from the metadata.

    Next, it checks if URI-R -> URI-M mappings exists for the PDF and if not, returns a ``400 Bad Request`` HTTP response.
    Upon doing so, it gets the last modified time of the URI-R -> URI-M mappings.
    Using this information, it generates the LDN payload and returns it with a ``200 OK`` HTTP response.

    :param pdf_hash: MD5 hash of an uploaded PDF
    :param ld_server_url: URL of the Linked Data (LD) Server
    :param ldp_inbox_url: URL of the LDP inbox of the given LD Server
    :return: An LDN as a JSON response

    """
    # assert that PDF exists
    pdf_path = os.path.join(self.app.config['UPLOADS_FOLDER'], pdf_hash + ".pdf")
    if not os.path.exists(pdf_path):
      return flask.abort(self.make_error_res(404, self.ERR_PDF_NOT_FOUND))
    # assert that PDF metadata exists
    pdf_meta_path = os.path.join(self.app.config['UPLOADS_FOLDER'], pdf_hash + ".pdf.txt")
    if not os.path.exists(pdf_meta_path):
      return flask.abort(self.make_error_res(404, self.ERR_PDF_META_NOT_FOUND))
    # get the original pdf name from metadata
    with open(pdf_meta_path) as f:
      pdf_name = f.readline()
    # assert that the URI-R -> URI-M mappings exist for the PDF
    mapping_path = os.path.join(self.app.config['MAPPING_FOLDER'], pdf_hash + ".pdf.json")
    if not os.path.exists(mapping_path):
      return flask.abort(self.make_error_res(404, self.ERR_MAPPING_NOT_FOUND))
    # last modified time of the URI-R -> URI-M mappings
    mapping_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(mapping_path)).isoformat()
    # generate LDN payload
    ldn_args = {
      'hostname': flask.request.host_url.strip(' /'),
      'pdf_hash': pdf_hash,
      'pdf_name': pdf_name,
      'created_time': datetime.datetime.now().isoformat(),
      'published_time': mapping_mtime,
      'ld_server_url': ld_server_url,
      'ldp_inbox_url': ldp_inbox_url
    }
    payload = flask.render_template("ldn.json", **ldn_args)
    # return LDN payload as JSON
    return flask.jsonify(flask.json.loads(payload))

  def get_req_payload_as_json(self):
    """
    Parse the request body as JSON, and return the parsed object.

    If the body cannot be parsed as JSON, it returns a ``400 Bad Request`` HTTP response.

    :return: Parsed Request body as an object

    """
    try:
      # try generating JSON from request body
      return flask.request.get_json()
    except json.JSONDecodeError:
      # if body is not JSON, abort request
      return flask.abort(self.make_error_res(400, self.ERR_REQ_NOT_JSON))

  def get_ld_server_url_from_req_payload(self, key='ld_server_url'):
    """
    Parse the request body as JSON, and return the LD server URL given in it.

    If the body cannot be parsed as JSON, or if ``key`` does not exist, it returns a ``400 Bad Request`` HTTP response.

    :param key: Key to extract from request body (default='ld_server_url`)
    :return: The LD Server URL given in the request body

    """
    # get request body as JSON
    req_json = self.get_req_payload_as_json()
    # assert that LD server URL exists in request body
    if key not in req_json:
      return flask.abort(self.make_error_res(400, self.ERR_MISSING_PARAM_LD_SERVER_URL))
    return req_json[key]

  def get_ld_server_url_from_query_params(self, key='ld_server_url'):
    """
    Parse the request query params and return the LD server URL given in it.

    If ``key`` does not exist in the request query params, it returns a ``400 Bad Request`` HTTP response.

    :param key: Key to extract from request query params (default='ld_server_url`)
    :return: The LD Server URL given in the request query params

    """
    # assert that LD server URL exists in request query params
    if key not in flask.request.args:
      return flask.abort(self.make_error_res(400, self.ERR_MISSING_PARAM_LD_SERVER_URL))
    # return LD server URL from request query params
    return flask.request.args.get(key)

  def resolve_ldp_inbox_url(self, ld_server_url: str):
    """
    Return the URL of the LDP inbox of the Linked Data (LD) service found at the ``ld_server_url``.

    This function performs a HEAD request to the ``ld_server_url``, and parses the link headers of the response.
    If a LDP inbox URL is found in the link header, it returns it.
    If not found, it returns a ``400 Bad Request`` HTTP response.

    :param ld_server_url: URL of the Linked Data (LD) server
    :return: The URL of the LDP inbox of the LD server

    """
    # Send HTTP HEAD request to LD Server URL
    res = requests.head(ld_server_url)
    # Get LDP Inbox URL from Link Header
    ldn_inbox_rel = "http://www.w3.org/ns/ldp#inbox"
    if ldn_inbox_rel not in res.links:
      return flask.abort(self.make_error_res(400, f"The URL {ld_server_url} is not an LD Server"))
    return res.links[ldn_inbox_rel]['url']
