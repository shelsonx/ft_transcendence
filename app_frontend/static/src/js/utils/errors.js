export const getErrorMessage = (error) => {
  switch (error) {
    case 400:
      return 'Bad Request'
    case 401:
      return 'Unauthorized'
    case 402:
      return 'Payment Required'
    case 403:
      return 'Forbidden'
    case 404:
      return 'Not Found'
    case 405:
      return 'Method Not Allowed'
    case 408:
      return 'Request Timeout'
    case 500:
      return 'Internal Server Error'
    case 501:
      return 'Not Implemented'
    case 502:
      return 'Bad Gateway'
    case 503:
      return 'Service Unavailable'
    case 504:
      return 'Gateway Timeout'
    default:
      return undefined;
  }
}

