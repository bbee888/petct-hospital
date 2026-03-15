import { loginRequest } from '../utils/request'

/**
 * 认证相关API
 */
export const authApi = {
  /**
   * 用户登录
   * @param {string} username - 用户名
   * @param {string} password - 密码
   * @returns {Promise<{access_token: string, token_type: string}>} 登录响应
   */
  async login(username, password) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await loginRequest.post('/v1/auth/login', formData)
    return response.data
  }
}

export default authApi