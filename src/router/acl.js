import { userStore } from '../stores/UserStore'
import { computed } from 'vue'
import { getUser } from '../api';

export async function acl() {
  const store = userStore()

  const user = await getUser()
  console.log(user);
  return user
} 

// Vue.use(AclInstaller)
// export default new AclCreate({
//   initial: 'public',
//   notfound: {
//     path: '/error',
//     forwardQueryParams: true,
//   },
//   router,
//   acceptLocalRules: true,
//   globalRules: {
//     isPublic: new AclRule('public').or('admin').generate(),
//     isAdmin: new AclRule('Role_admin').generate(),
//     isAffiliate: new AclRule('Role_affiliate').generate(),
//     isDirectSale: new AclRule('Role_direct_sale').generate(),
//     isLogged: new AclRule('user').and('inside').generate()
//   },
//   middleware: async acl => {
//     await timeout(2000) // call your api
//     acl.change('admin')
//   }
// })