import axios from 'axios'


// axios.defaults.withCredentials = true
// axios.defaults.baseURL = "http://"

export default {
    fetchUsers: () => {
        let response = null

        axios.get('/admin/users/list').then(res => response = res.data)
    }
}