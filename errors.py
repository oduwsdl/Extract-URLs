class URLError(Exception):
  """
  The ``URLError`` is raised when a URL-like string extracted from a PDF
  is determined a non-URL (i.e., a false positive).

  :param url: URL-like string that was determined a non-URL
  :param args: Optional arguments to propagate into the base ``Exception`` class.

  """

  def __init__(self, url: str, *args: object) -> None:
    super().__init__(*args)
    self.url = url

  def __str__(self) -> str:
    return f"Invalid URL: {self.url}"
