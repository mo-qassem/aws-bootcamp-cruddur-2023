# Week 3 — Decentralized Authentication

### Homework Tasks

| TASKS                                               | COMPLETED          |
| --------------------------------------------------- | ------------------ |
| Setup Cognito User Pool.                            | :heavy_check_mark: |
| Implement Custom Signin Page.                       | :heavy_check_mark: |
| Implement Custom Signup Page.                       | :heavy_check_mark: |
| Implement Custom Confirmation Page.                 | :heavy_check_mark: |
| Implement Custom Recovery Page.                     | :heavy_check_mark: |
| Watch about different approaches to verifying JWTs. | :heavy_check_mark: |

---

## 1. Setup Cognito User Pool.

```
Checkbox for below Required Attributes:
- Name
- Preferred_username
```

![cognito_userpool](/journal/screenshots/week3_cognito.png)

- ### Install `AWS-Amplify` library

  ```shell
  cd frontend-react-js
  npm install aws-amplify --save
  ```

- ### Configure `AWS-Amplify` in `App.js`

  ```javascript
  //----------------AWS-Amplify Global Config----------------------
  import { Amplify } from "aws-amplify";
  Amplify.configure({
    AWS_PROJECT_REGION: process.env.REACT_APP_AWS_PROJECT_REGION,
    aws_cognito_region: process.env.REACT_APP_AWS_COGNITO_REGION,
    aws_user_pools_id: process.env.REACT_APP_AWS_USER_POOLS_ID,
    aws_user_pools_web_client_id: process.env.REACT_APP_CLIENT_ID,
    oauth: {},
    Auth: {
      // We are not using an Identity Pool
      // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
      region: process.env.REACT_APP_AWS_PROJECT_REGION, // REQUIRED - Amazon Cognito Region
      userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID, // OPTIONAL - Amazon Cognito User Pool ID
      userPoolWebClientId: process.env.REACT_APP_CLIENT_ID, // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
    },
  });
  ```

- ### Add below env-vars to `cruddur-frontend-reactjs` service in `docker-compose.yaml`

  ```yaml
  REACT_APP_AWS_PROJECT_REGION: "${AWS_DEFAULT_REGION}"
  REACT_APP_AWS_COGNITO_REGION: "${AWS_DEFAULT_REGION}"
  REACT_APP_AWS_USER_POOLS_ID: "${AWS_USER_POOLS_ID}"
  REACT_APP_CLIENT_ID: "${AWS_APP_CLIENT_ID}"
  ```

- ### Conditionally show informations based on logIn or LogOut in `HomeFeedPage.js`
  - Import `Auth` Function from `aws-amplify`
    ```javascript
    import { Auth } from "aws-amplify";
    ```
  - Write below function to check `authenticated_user`
    ```javascript
    //-----------check if we are authenicated---------------
    const checkAuth = async () => {
      Auth.currentAuthenticatedUser({
        // Optional, By default is false.
        // If set to true, this call will send a
        // request to Cognito to get the latest user data
        bypassCache: false,
      })
        .then((user) => {
          console.log("user", user);
          return Auth.currentAuthenticatedUser();
        })
        .then((cognito_user) => {
          setUser({
            display_name: cognito_user.attributes.name,
            handle: cognito_user.attributes.preferred_username,
          });
        })
        .catch((err) => console.log(err));
    };
    ```
- ### Update authentication config in `ProfileInfo.js`
  - Import `Auth` Function from `aws-amplify`
    ```javascript
    import { Auth } from "aws-amplify";
    ```
  - Update `SignOut` funcion
    ```javascript
    const signOut = async () => {
      try {
        await Auth.signOut({ global: true });
        window.location.href = "/";
      } catch (error) {
        console.log("error signing out: ", error);
      }
    };
    ```

## 02. Implement Custom Signin Page.

- ### Update authentication config in `SigninPage.js`
  - Import `Auth` Function from `aws-amplify`
    ```javascript
    import { Auth } from "aws-amplify";
    ```
  - Update `onsubmit` function
    ```javascript
    const onsubmit = async (event) => {
      setErrors("");
      event.preventDefault();
      Auth.signIn(email, password)
        .then((user) => {
          localStorage.setItem(
            "access_token",
            user.signInUserSession.accessToken.jwtToken
          );
          window.location.href = "/";
        })
        .catch((error) => {
          if (error.code == "UserNotConfirmedException") {
            window.location.href = "/confirm";
          }
          setErrors(error.message);
        });
      return false;
    };
    ```

## 03. Implement Custom `SignupPage.js`.

- ### Import `Auth` Function from `aws-amplify`
  ```javascript
  import { Auth } from "aws-amplify";
  ```
- ### Update `onsubmit` function
  ```javascript
  const onsubmit = async (event) => {
    event.preventDefault();
    setErrors("");
    try {
      const { user } = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
          name: name,
          email: email,
          preferred_username: username,
        },
        autoSignIn: {
          // optional - enables auto sign in after user is confirmed
          enabled: true,
        },
      });
      console.log(user);
      window.location.href = `/confirm?email=${email}`;
    } catch (error) {
      console.log(error);
      setErrors(error.message);
    }
    return false;
  };
  ```

## 04. Implement Custom `ConfirmationPage.js`.

- ### Import `Auth` Function from `aws-amplify`
  ```javascript
  import { Auth } from "aws-amplify";
  ```
- ### Update `resend_code` function
  ```javascript
  const resend_code = async (event) => {
    setErrors("");
    try {
      await Auth.resendSignUp(email);
      console.log("code resent successfully");
      setCodeSent(true);
    } catch (err) {
      // does not return a code
      // does cognito always return english
      // for this to be an okay match?
      console.log(err);
      if (err.message == "Username cannot be empty") {
        setErrors(
          "You need to provide an email in order to send Resend Activiation Code"
        );
      } else if (err.message == "Username/client id combination not found.") {
        setErrors("Email is invalid or cannot be found.");
      }
    }
  };
  ```
- ### Update `onsubmit` function
  ```javascript
  const onsubmit = async (event) => {
    event.preventDefault();
    setErrors("");
    try {
      await Auth.confirmSignUp(email, code);
      window.location.href = "/";
    } catch (error) {
      setErrors(error.message);
    }
    return false;
  };
  ```
- ### Auto fill-in Email value

  ```javascript
  import { useLocation } from "react-router-dom";
  ```

  ```javascript
  const location = useLocation();
  React.useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const emailParam = searchParams.get("email");
    if (emailParam) {
      setEmail(emailParam);
    }
  }, [location]);
  ```

## 05. Implement Custom `RecoverPage.js`.

- ### Import `Auth` Function from `aws-amplify`
  ```javascript
  import { Auth } from "aws-amplify";
  ```
- ### Update `onsubmit_send_code` function
  ```javascript
  const onsubmit_send_code = async (event) => {
    event.preventDefault();
    setErrors("");
    Auth.forgotPassword(username)
      .then((data) => setFormState("confirm_code"))
      .catch((err) => setErrors(err.message));
    return false;
  };
  ```
- ### Update `onsubmit_confirm_code` function
  ```javascript
  const onsubmit_confirm_code = async (event) => {
    event.preventDefault();
    setErrors("");
    if (password == passwordAgain) {
      Auth.forgotPasswordSubmit(username, code, password)
        .then((data) => setFormState("success"))
        .catch((err) => setErrors(err.message));
    } else {
      setErrors("Passwords do not match");
    }
    return false;
  };
  ```

## 06. Verifying `JWT-TOKEN` through backend

- ### Update `CORS` configuration in `app.py`
  ```python
  cors = CORS(
  app,
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'],
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
  )
  ```
- ### Update `requirements.txt` and
  ```shell
  Flask-AWSCognito
  ```
- ### Add below env-vars for `cruddur-backend-flask` service in `docker-compose.yaml`

  ```yaml
  AWS_COGNITO_USER_POOL_ID: "${AWS_USER_POOLS_ID}"
  AWS_COGNITO_USER_POOL_CLIENT_ID: "${AWS_APP_CLIENT_ID}"
  ```

- ### Write our own library `service` to verify JWT Token

  ```python
  import time
  import requests
  from jose import jwk, jwt
  from jose.exceptions import JOSEError
  from jose.utils import base64url_decode

  class FlaskAWSCognitoError(Exception):
      pass
  class TokenVerifyError(Exception):
      pass


  class CognitoJwtVerification:
      def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
          self.region = region
          if not self.region:
              raise FlaskAWSCognitoError("No AWS region provided")
          self.user_pool_id = user_pool_id
          self.user_pool_client_id = user_pool_client_id
          self.claims = None
          if not request_client:
              self.request_client = requests.get
          else:
              self.request_client = request_client
          self._load_jwk_keys()

      @classmethod
      def extract_access_token(request_headers):
          access_token = None
          auth_header = request_headers.get("Authorization")
          if auth_header and " " in auth_header:
              _, access_token = auth_header.split()
          return access_token

      def _load_jwk_keys(self):
          keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
          try:
              response = self.request_client(keys_url)
              self.jwk_keys = response.json()["keys"]
          except requests.exceptions.RequestException as e:
              raise FlaskAWSCognitoError(str(e)) from e

      @staticmethod
      def _extract_headers(token):
          try:
              headers = jwt.get_unverified_headers(token)
              return headers
          except JOSEError as e:
              raise TokenVerifyError(str(e)) from e

      def _find_pkey(self, headers):
          kid = headers["kid"]
          # search for the kid in the downloaded public keys
          key_index = -1
          for i in range(len(self.jwk_keys)):
              if kid == self.jwk_keys[i]["kid"]:
                  key_index = i
                  break
          if key_index == -1:
              raise TokenVerifyError("Public key not found in jwks.json")
          return self.jwk_keys[key_index]

      @staticmethod
      def _verify_signature(token, pkey_data):
          try:
              # construct the public key
              public_key = jwk.construct(pkey_data)
          except JOSEError as e:
              raise TokenVerifyError(str(e)) from e
          # get the last two sections of the token,
          # message and signature (encoded in base64)
          message, encoded_signature = str(token).rsplit(".", 1)
          # decode the signature
          decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
          # verify the signature
          if not public_key.verify(message.encode("utf8"), decoded_signature):
              raise TokenVerifyError("Signature verification failed")

      @staticmethod
      def _extract_claims(token):
          try:
              claims = jwt.get_unverified_claims(token)
              return claims
          except JOSEError as e:
              raise TokenVerifyError(str(e)) from e

      @staticmethod
      def _check_expiration(claims, current_time):
          if not current_time:
              current_time = time.time()
          if current_time > claims["exp"]:
              raise TokenVerifyError("Token is expired")  # probably another exception

      def _check_audience(self, claims):
          # and the Audience  (use claims['client_id'] if verifying an access token)
          audience = claims["aud"] if "aud" in claims else claims["client_id"]
          if audience != self.user_pool_client_id:
              raise TokenVerifyError("Token was not issued for this audience")

      def verify(self, token, current_time=None):
          """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
          if not token:
              raise TokenVerifyError("No token provided")

          headers = self._extract_headers(token)
          pkey_data = self._find_pkey(headers)
          self._verify_signature(token, pkey_data)

          claims = self._extract_claims(token)
          self._check_expiration(claims, current_time)
          self._check_audience(claims)

          self.claims = claims
          return claims
  ```

- ### Add below `app = Flask(__name__)` configuring our new library

  ```python
  cognito_jwt_verification = CognitoJwtVerification.new(
  user_pool_id=os.getenv("AWS_USER_POOLS_ID"),
  user_pool_client_id=os.getenv("AWS_APP_CLIENT_ID"),
  region=os.getenv("AWS_DEFAULT_REGION")
  )
  ```

- ### Configure `home_activities.py` to verify what data will be visable when user hit below api endpoint and what data will display if user is authenticated or not.

  ```python
  @app.route("/api/activities/home", methods=['GET'])
  def data_home():
  access_token = extract_access_token(request.headers)
  try:
  #------------Authenticated Request-----------
      claims = cognito_jwt_verification.verify(access_token)
      app.logger.debug('Authenticated Request')
      app.logger.debug(claims['username'])
      data = HomeActivities.run(cognito_user_id=claims['username'], Logger=LOGGER )
  #------------Un-Authenticated Request-----------
  except TokenVerifyError as e:
          app.logger.debug('Un-Authenticated Request')
          data = HomeActivities.run(Logger=LOGGER)
  #---------------Display Auth header from frontend-------------
  app.logger.debug('Authorization HEADER')
  app.logger.debug(
      request.headers.get('Authorization')
  )
  #------------------------------------------------------------
  data = HomeActivities.run(Logger=LOGGER)
  return data, 200
  ```

- ### Update `ProfileInfo.js` to remove JWT-Tokon from localstorage when user signout by adding the below line of code to `SignOut` function
  ```javascript
  localStorage.removeItem("access_token");
  ```

---

### Homework Challenges

| TASKS                                                                                                                                                               | COMPLETED                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| [Medium] Decouple the JWT verify from the application code by writing a Flask Middleware                                                                            | :heavy_exclamation_mark: |
| [Hard] Decouple the JWT verify by implementing a Container Sidecar pattern using AWS’s official Aws-jwt-verify.js library.                                          | :heavy_exclamation_mark: |
| [Hard] Decouple the JWT verify process by using Envoy as a sidecar https://www.envoyproxy.io/.                                                                      | :heavy_exclamation_mark: |
| [Hard] Implement a IdP login eg. Login with Amazon or Facebook or Apple.                                                                                            | :heavy_exclamation_mark: |
| [Easy] Implement MFA that send an SMS (text message), warning this has spend, investigate spend before considering, text messages are not eligible for AWS Credits. | :heavy_exclamation_mark: |

```

```

```

```

```

```

```

```

```

```
