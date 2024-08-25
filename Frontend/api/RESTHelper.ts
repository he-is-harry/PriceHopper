import { BASE_API_URL } from "@env";

export async function getAPIData(apiPath: string) {
    return fetch(`${BASE_API_URL}${apiPath}`, {
        method: "GET",
        headers: {
            Accept: "application/json"
        }
    }).then(async (response) => {
        return await response.json();
    });
}

export async function postAPIData(apiPath: string, body) {
    return fetch(`${BASE_API_URL}${apiPath}`, {
        method: "POST",
        headers: {
            Accept: "application/json",
            'Content-Type': "application/json"
        },
        body: JSON.stringify(body)
    }).then(async (response) => {
        return await response.json();
    });
}

