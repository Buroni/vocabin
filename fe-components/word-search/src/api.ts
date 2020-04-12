import axios from "axios";
import env from "./env";
import { buildQueryString } from "./utils";
import Cookies from "js-cookie";

// Default config options
const defaultOptions = {
    baseURL: env.baseURL,
    headers: {
      'Content-Type': 'application/json',
    },
};

class VocaAPI {

    private readonly api;

    public constructor() {
        this.initAPI();
    }

    private initAPI() {
        this.api = axios.create(defaultOptions);
            // Set the AUTH token for any request
            this.api.interceptors.request.use(function (config) {
                config.headers["X-CSRFToken"] = Cookies.get("csrftoken");
                return config;
            });
    }

    public get(path, queryParams) {
        return this.api.get(`${path}?${buildQueryString(queryParams)}`)
    }

    public post(path, body) {
        return this.api.post(path, body);
    }
}

const VocaAPIInstance = new VocaAPI();

export default VocaAPIInstance;
