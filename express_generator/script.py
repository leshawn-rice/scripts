import os


def create_folders():
    os.mkdir('./routes')
    os.mkdir('./models')
    os.mkdir('./__tests__')
    os.mkdir('./helpers')
    os.mkdir('./middleware')


def install_dependencies():
    os.system('npm i express cors dotenv morgan')


def create_package_json():
    with open('package.json', 'w') as package_file:
        package_file.write(
            '{\n  "name": "project-name",\n  "version": "project-version",\n  "description": "",\n  "main": "server.js",\n  "scripts": {\n    "start": "node server.js",\n    "dev": "nodemon server.js",\n    "test": "jest -i"\n  },\n  "jest": {\n    "testPathIgnorePatterns": [\n      "/node_modules/","config.js","common.js"\n    ]\n  },\n  "keywords": [],\n  "author": "",\n  "license": "ISC"\n}'
        )


def create_error_file():
    with open('expressError.js', 'w') as error_file:
        error_file.write(
            '/** ExpressError extends normal JS error so we can\n*  add a status when we make an instance of it.\n*\n*  The error-handling middleware will return this.\n*/\n\nclass ExpressError extends Error {\n  constructor(message, status) {\n    super();\n    this.message = message;\n    this.status = status;\n  }\n}\n\n/** 404 NOT FOUND error. */\nclass NotFoundError extends ExpressError {\n  constructor(message = "Not Found") {\n    super(message, 404);\n  }\n}\n\n/** 401 UNAUTHORIZED error. */\nclass UnauthorizedError extends ExpressError {\n  constructor(message = "Unauthorized") {\n    super(message, 401);\n  }\n}\n\n/** 400 BAD REQUEST error. */\nclass BadRequestError extends ExpressError {\n  constructor(message = "Bad Request") {\n    super(message, 400);\n  }\n}\n\n/** 403 BAD REQUEST error. */\nclass ForbiddenError extends ExpressError {\n  constructor(message = "Bad Request") {\n    super(message, 403);  }\n}\n\n/** 500 INTERNAL SERVER error */\nclass InternalServerError extends ExpressError {\n  constructor(message = "Internal Server Error") {\n    super(message, 500);\n  }\n}\n\nmodule.exports = {\nExpressError,\nNotFoundError,\nUnauthorizedError,\nBadRequestError,\nForbiddenError,\n};'
        )


def create_server_file():
    with open('server.js', 'w') as server_file:
        server_file.write(
            '"use strict";\n\nconst app = require(\'./app\');\nconst { PORT } = (\'./config\');\n\napp.listen(PORT, function () {\n  console.log(`Started on http://localhost:${PORT}`);\n});'
        )


def create_config_file():
    with open('config.js', 'w') as config_file:
        config_file.write(
            '"use strict";\n\nrequire("dotenv").config();\n\nconst SECRET_KEY = process.env.SECRET_KEY || "secret-dev";\nconst PORT = +process.env.PORT || 3001;\n\n// Use dev database, testing database, or via env var, production database\nfunction getDatabaseUri() {\n  return (process.env.NODE_ENV === "test") ? "DB_NAME_test" : process.env.DATABASE_URL || "DB_NAME";\n}\n\nconst BCRYPT_WORK_FACTOR = process.env.NODE_ENV === "test" ? 1 : 12;\n\nmodule.exports = {\n  SECRET_KEY,\n  PORT,\n  BCRYPT_WORK_FACTOR,\n  getDatabaseUri,\n};'
        )


def create_db_file():
    with open('db.js', 'w') as db_file:
        db_file.write(
            '"use strict";\n\n/** Database setup for DB_NAME. */\nconst { Client } = require("pg");\nconst { getDatabaseUri } = require("./config");\nconst db = new Client({\n  connectionString: getDatabaseUri(),\n});\n\ndb.connect();\n\nmodule.exports = db;'
        )


def create_app_file():
    with open('app.js', 'w') as app_file:
        app_file.write(
            '"use strict";\n\n// External Dependencies\nconst express = require("express");\n// Internal Dependencies\nconst { NotFoundError } = require("./expressError");\n\nconst app = express();\n\napp.use(express.json());\n\n/** Handle 404 errors -- this matches everything */\napp.use(function (req, res, next) {\n  return next(new NotFoundError());\n});\n\n/** Generic error handler; anything unhandled goes here. */\napp.use(function (err, req, res, next) {\n  if (process.env.NODE_ENV !== \'test\') console.error(err.stack);\n  const status = err.status || 500;\n  const message = err.message;\n\n  return res.status(status).json({\n    error: { message, status },\n  });\n});\n\nmodule.exports = app;'
        )


# Need to add an input for database name, test database name, app name, default PORT, and default SECRET KEY

# Need to add some default tests, default middleware (JWT auth etc)

def main():
    # Create a config.js file
    create_config_file()
    # Create a server.js file
    create_server_file()
    # Create an app.js file
    create_app_file()
    # Create a db.js file
    create_db_file()
    # Create an error file
    create_error_file()
    # Create a package.json file
    create_package_json()
    # Create the folders
    create_folders()
    # Install dependencies
    install_dependencies()


if __name__ == '__main__':
    main()
