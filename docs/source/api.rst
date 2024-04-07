API
===
Liveness Probe
--------------

The liveness probe endpoint is used to check the health of the application. It returns a success code if the application is running.

.. code-block:: python

    @probe_router.get("/liveness")
    def liveness():
        # Returns a success code and a 'HI' message if the application is alive
        return {"code": SystemResponseCode.SUCCESS.code, "msg": "hi"}

Readiness Probe
---------------

The readiness probe endpoint checks if the application is ready to handle requests. It attempts to perform a sample user service action.

.. code-block:: python

    # Readiness probe
    @probe_router.get("/readiness")
    async def readiness(user_service: UserService = Depends(get_user_service)):
        try:
            # Tries to find a user by ID to verify database interaction
            await user_service.find_by_id(USER_ID)
        except Exception as e:
            # Logs the exception and returns a service internal error code and message
            logger.error(f"readiness error: {e}")
            return {
                "code": SystemResponseCode.SERVICE_INTERNAL_ERROR.code,
                "msg": SystemResponseCode.SERVICE_INTERNAL_ERROR.msg,
            }

        # Returns a success code and a 'HELLO' message if the service is ready
        return {"code": SystemResponseCode.SUCCESS.code, "msg": "hello"}

User Registration
-----------------

User registration endpoint allows new users to create an account. The password is hashed before saving the user.

.. code-block:: python

    @user_router.post("/register")
    async def create_user(
        create_data: UserCreateCmd, user_service: UserService = Depends(get_user_service)
    ) -> BaseResponse[int]:
        create_data.password = await get_password_hash(create_data.password)
        user: UserDO = await user_service.save(data=create_data)
        return result.success(data=user.id)

Query User Information
----------------------

This endpoint retrieves the current user's information based on their authentication status.

.. code-block:: python

    # Query user info
    @user_router.get("/me")
    async def get_user(
        user_service: UserService = Depends(get_user_service),
        current_user: CurrentUser = Depends(get_current_user()),
    ) -> BaseResponse[UserQuery]:
        user: UserQuery = await user_service.find_by_id(id=current_user.user_id)
        return result.success(data=user)

User Login
----------

The login endpoint authenticates users and returns a token upon successful login.

.. code-block:: python

    # User login
    @user_router.post("/login")
    async def login(
        login_form: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(get_user_service),
    ) -> Token:
        loginCmd = LoginCmd(username=login_form.username, password=login_form.password)
        return await user_service.login(loginCmd)
