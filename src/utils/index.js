
export function is_authenticated(){
    let cookie = document.cookie
    if(!cookie)
        return false
    return true
}