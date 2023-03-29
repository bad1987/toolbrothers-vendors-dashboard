import axios from "axios"
import { createBlock } from "vue"

export function is_authenticated(){
    let cookie = document.cookie
    if(!cookie)
        return false
    return true
}

export function local_storage_set(key, value){
    localStorage.setItem(key, value)
}

export function local_storage_get(key){
    return localStorage.getItem(key)
}

export function refresh_token(){
    // get the expire timestamp and convert in minutes
    let cookie_age = parseInt(local_storage_get(local_storage_get('cookie_name')))
    cookie_age = parseInt(cookie_age/60000)
    // get current timestamp and convert in minutes
    let current_age = new Date().getTime()
    current_age = parseInt(current_age/60000)
    // console.log(`max-age:${cookie_age} cuurent-age:${current_age}`)
    let diff = cookie_age - current_age
    if(diff > 0 && diff <= 1){
        // console.log("It is time to refresh the token")
        let url = axios.defaults.baseURL + 'auth/refresh'
        axios.get(url)
            .then(res=>{
                let data = res.data;
                let token_type = data.token_type.charAt(0).toUpperCase() + data.token_type.slice(1);
                let cookie_val = `${token_type} ${data[data.cookie_name]}`
                let time = data.expired_at * 60;
                let temp = `${data.cookie_name}=${cookie_val}; max-age=${time}; SameSite=None; Secure`;
                document.cookie = temp;
                //TODO::save the cookie max-age for later use(refresh token)
                local_storage_set('cookie_name', data.cookie_name)
                local_storage_set(data.cookie_name, new Date().getTime() + time*1000)
            })
            .catch(err=>{
                if(err.response.data){
                    console.log(err.response.data)
                }
                else{
                    console.log(err)
                }
            })
    }
    else if(diff <= 0){
        // console.log("It is time to log in your cookie expired")
    }
    else{
        // console.log("No refresh need ")
    }
}