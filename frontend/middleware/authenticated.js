export default function ({ store, redirect }) {
  // ユーザーが認証されていないとき
  if (!store.state.user.login) {
    return redirect('/')
  }
}
