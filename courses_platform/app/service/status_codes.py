from app.response_objects import ResponseFailure, ResponseSuccess


STATUS_CODES = {
    ResponseSuccess.SUCCESS_OK: 200,
    ResponseSuccess.SUCCESS_RESOURCE_CREATED: 201,
    ResponseSuccess.SUCCESS_NO_CONTENT: 204,
    ResponseFailure.RESOURCE_ERROR: 404,
    ResponseFailure.SYSTEM_ERROR: 500
}
