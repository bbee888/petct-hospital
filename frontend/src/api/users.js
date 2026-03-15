import request from '../utils/request'

/**
 * 用户管理相关API
 */
export const usersApi = {
  /**
   * 获取用户列表
   * @returns {Promise} 用户列表
   */
  async getUsers() {
    const response = await request.get('/v1/users/')
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 获取单个用户
   * @param {number} id - 用户ID
   * @returns {Promise} 用户详情
   */
  async getUser(id) {
    const response = await request.get(`/v1/users/${id}`)
    return response.data
  },

  /**
   * 创建用户
   * @param {Object} userData - 用户数据
   * @returns {Promise} 创建结果
   */
  async createUser(userData) {
    const response = await request.post('/v1/users/', userData)
    return response.data
  },

  /**
   * 更新用户
   * @param {number} id - 用户ID
   * @param {Object} userData - 用户数据
   * @returns {Promise} 更新结果
   */
  async updateUser(id, userData) {
    const response = await request.put(`/v1/users/${id}`, userData)
    return response.data
  },

  /**
   * 删除用户
   * @param {number} id - 用户ID
   * @returns {Promise} 删除结果
   */
  async deleteUser(id) {
    const response = await request.delete(`/v1/users/${id}`)
    return response.data
  }
}

export default usersApi
