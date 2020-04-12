const env = {
    "development": {
        baseURL: "http://localhost:8000/api/"
    },
    "production": {
        baseURL: "http://104.247.76.243/api/"
    }
}

export default env[process.env.NODE_ENV || "development"]
