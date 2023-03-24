import { defineStore } from "pinia";
import { getUser } from '../api'
export let userStore = defineStore("user", {
    state: () => ({
        "user": null
    }),

    // actions
    actions: {
        async init(){
            getUser(this.setUser)
        },
        setUser(user){
            if(user)
                this.user = user
        }
    },
})