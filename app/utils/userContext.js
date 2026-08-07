export function getUserId() {
  let userId = localStorage.getItem('vwo_user_id');

  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('vwo_user_id', userId);
  }

  return userId;
}
