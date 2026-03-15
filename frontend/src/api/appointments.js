import request from '../utils/request'

/**
 * 预约管理相关API
 */
export const appointmentsApi = {
  /**
   * 获取预约列表
   * @returns {Promise} 预约列表
   */
  async getAppointments() {
    const response = await request.get('/v1/appointments/')
    return {
      data: response.data || [],
      total: (response.data || []).length
    }
  },

  /**
   * 获取单个预约
   * @param {number} id - 预约ID
   * @returns {Promise} 预约详情
   */
  async getAppointment(id) {
    const response = await request.get(`/v1/appointments/${id}`)
    return response.data
  },

  /**
   * 更新预约
   * @param {number} id - 预约ID
   * @param {Object} data - 更新数据
   * @returns {Promise} 更新结果
   */
  async updateAppointment(id, data) {
    const response = await request.put(`/v1/appointments/${id}`, data)
    return response.data
  },

  /**
   * 删除预约
   * @param {number} id - 预约ID
   * @returns {Promise} 删除结果
   */
  async deleteAppointment(id) {
    const response = await request.delete(`/v1/appointments/${id}`)
    return response.data
  }
}

export default appointmentsApi
