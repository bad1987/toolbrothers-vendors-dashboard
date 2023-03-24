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

export function interceptor(){
    // Request interceptors for API calls
    axios.interceptors.request.use(
        config => {
        // config.headers['Accept'] = 'application/json';
        // config.headers['Content-Type'] = 'application/json'
        config.headers['withCredentials'] = true;
        // config.headers['Authorization'] = getCookie('access_token');
            return config;
        },
        error => {
            return Promise.reject(error);
        }
    );
}

export function getCookie(name) {
    var pair = document.cookie.split('; ').find(x => x.startsWith(name+'='));
    if (pair)
       return pair.split('=')[1]
}

export function getUser(setter =null){
    const url = axios.defaults.baseURL + 'admin/user'
    axios.get(url)
        .then(response => {
            if(setter){
                setter(response.data.user)
            }
            return response.data.user
        })
        .catch(err => {
            // pass
            console.log(err)
            return null
        })
}