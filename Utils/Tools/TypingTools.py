from typing import TypedDict, List, Dict, Union

class APIType(TypedDict):
    version: str
    routeKey: str
    rawPath: str
    rawQueryString: Union[str, None]
    cookies: List[str]
    headers: Dict[str, str]
    queryStringParameters: Union[Dict[str, str], None]
    requestContext: Union[Dict[str, str], Dict[str, dict]]
    body: Union[str, None]
    pathParameters: Union[dict, None]
    isBase64Encoded: bool
    stageVariables: Union[dict, None]

EventType = APIType