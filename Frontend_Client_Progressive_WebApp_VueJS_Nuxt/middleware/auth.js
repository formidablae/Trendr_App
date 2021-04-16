export default function({ store, redirect, app }) {
  // if (!store.state.auth.loggedIn) {
  if(false) {
    return redirect(app.localePath('/login'))
  }
}
