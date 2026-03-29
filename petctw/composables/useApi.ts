// API调用模块 - 对接后端API
// 后端API前缀: /api/v1

// 使用后端服务器地址
const API_BASE = 'http://127.0.0.1:8001/api/v1'

// 站点域名 - 用于筛选对应站点的数据
const SITE_DOMAIN = 'www.petctw.com'

// 通用请求方法
async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  const fullUrl = `${API_BASE}${url}`
  
  const response = await fetch(fullUrl, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    }
  })
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '请求失败' }))
    throw new Error(error.detail || '请求失败')
  }
  
  return response.json()
}

// 医院相关API
export const hospitalApi = {
  // 获取医院列表
  getList: async (params: {
    page?: number
    size?: number
    title?: string
    province_id?: number
    city_id?: number
    level?: string
    is_cooperation?: number
  } = {}) => {
    const queryParams = new URLSearchParams()
    if (params.page) queryParams.set('page', String(params.page))
    if (params.size) queryParams.set('size', String(params.size))
    if (params.title) queryParams.set('title', params.title)
    if (params.province_id) queryParams.set('province_id', String(params.province_id))
    if (params.city_id) queryParams.set('city_id', String(params.city_id))
    if (params.level) queryParams.set('level', params.level)
    if (params.is_cooperation !== undefined) queryParams.set('is_cooperation', String(params.is_cooperation))
    
    const query = queryParams.toString() ? `?${queryParams.toString()}` : ''
    return request<{ items: any[], total: number, page: number, size: number }>(`/hospitals${query}`)
  },
  
  // 获取医院详情
  getDetail: async (id: number) => {
    return request<any>(`/hospitals/${id}`)
  },
  
  // 获取热门医院（is_cooperation=1）
  getHotList: async (size: number = 6) => {
    return hospitalApi.getList({ page: 1, size, is_cooperation: 0 })
  }
}

// 文章相关API
export const articleApi = {
  // 获取文章列表
  getList: async (params: {
    title?: string
    category_id?: number
  } = {}) => {
    const queryParams = new URLSearchParams()
    // 添加站点域名筛选
    queryParams.set('site_domain', SITE_DOMAIN)
    if (params.title) queryParams.set('title', params.title)
    if (params.category_id) queryParams.set('category_id', String(params.category_id))
    
    return request<any[]>(`/articles?${queryParams.toString()}`)
  },
  
  // 获取文章详情
  getDetail: async (id: number) => {
    return request<any>(`/articles/${id}`)
  },
  
  // 获取最新文章
  getLatestList: async (size: number = 5) => {
    const queryParams = new URLSearchParams()
    queryParams.set('site_domain', SITE_DOMAIN)
    return request<any[]>(`/articles?${queryParams.toString()}`)
  }
}

// 预约相关API
export const appointmentApi = {
  // 创建预约
  create: async (data: {
    hospital_id: number
    username: string
    phone: string
    idcard?: string
    sex?: string
    appoint_date: string
    intro?: string
  }) => {
    return request<any>('/appointments', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }
}

// 地区相关API
export const geoApi = {
  // 获取省份列表
  getProvinces: async () => {
    return request<any[]>('/geo/provinces')
  },
  
  // 获取城市列表
  getCities: async (provinceId?: number) => {
    if (provinceId) {
      return request<any[]>(`/geo/cities?province_id=${provinceId}`)
    }
    return request<any[]>('/geo/cities')
  },
  
  // 获取地区树形结构
  getTree: async () => {
    return request<any[]>('/geo/tree')
  }
}
