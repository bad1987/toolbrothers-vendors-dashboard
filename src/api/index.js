import axios from 'axios'

export function api(url, method, params) {
    let response = null

    axios({
        url,
        method,
        data: params
    }).then (res => {
        response = res.data
    }).catch (err => {
        response = err
    })

    return response
}