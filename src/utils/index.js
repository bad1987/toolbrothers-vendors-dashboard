
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