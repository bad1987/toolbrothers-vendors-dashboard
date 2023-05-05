import axios from 'axios'
import { initFlowbite, initModals } from 'flowbite'
import { useRoute, useRouter } from 'vue-router'

const userApi = {
    fetchUsers: async (users, permissions, router, route) => {
        axios.get(`/admin/users/${route.params.type}/list`).then((response) => {
            users.value = response.data.users
            permissions.value = response.data.permissions
        }).then(() => {
            initFlowbite()
        })
        .catch(err => {
            if (err.response) {
                let status = err.response.status
                if (status) {
                    if (status == 403) {
                        // console.log(err.response.status);
                        router.push('/error/403')
                    }
                    else if (status == 401) {
                        router.push('/login')
                    }
                }
            }
        })
    },

    addUser: async (newUser, selectedPermissions, route) => {
        newUser.value.permissions = selectedPermissions

        if (route.params.type === 'admins') {
            newUser.value.roles = 'Role_admin'
        }

        return axios.post('admin/users', {
            username: newUser.value.username,
            email: newUser.value.email,
            status: newUser.value.status == true ? 'A' : 'D',
            permissions: newUser.value.permissions,
            roles: newUser.value.roles,
        })
    },

    updateUser: async (obj, users, selectedUser, selectedPermissions) => {
        if (selectedUser.value !== undefined && obj == null) {
            const datas = {...selectedUser.value,
                 permissions: selectedPermissions.value,
                 status: selectedUser.value.status
                }
            axios.put("admin/users/" + selectedUser.value.id, datas)
            .then(response => {
                let ans = users.value.map(x => x.id === selectedUser.value.id ? response.data : x)
                users.value = ans

                document.getElementById('edit-user-modal')?.click()

            })
            .catch(err => {
                console.log(err)
            })
        } else if (obj != null) {
            axios.put("admin/users/" + selectedUser.value.id, obj)
            .then(response => {
                let ans = users.value.map(x => x.id === selectedUser.value.id ? response.data : x)
                users.value = ans

                document.getElementById('edit-user-modal')?.click()

            }).then()
            .catch(err => {
                console.log(err)
            })
        }
    }
}


export {
    userApi
}