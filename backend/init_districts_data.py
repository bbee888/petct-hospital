import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import async_session
from app.models.geo import Province, City, District

# 四个直辖市的区县数据
municipality_districts = {
    "北京市": [
        "东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区",
        "门头沟区", "房山区", "通州区", "顺义区", "昌平区", "大兴区",
        "怀柔区", "平谷区", "密云区", "延庆区"
    ],
    "天津市": [
        "和平区", "河东区", "河西区", "南开区", "河北区", "红桥区",
        "东丽区", "西青区", "津南区", "北辰区", "武清区", "宝坻区",
        "滨海新区", "宁河区", "静海区", "蓟州区"
    ],
    "上海市": [
        "黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区",
        "杨浦区", "闵行区", "宝山区", "嘉定区", "浦东新区", "金山区",
        "松江区", "青浦区", "奉贤区", "崇明区"
    ],
    "重庆市": [
        "万州区", "涪陵区", "渝中区", "大渡口区", "江北区", "沙坪坝区",
        "九龙坡区", "南岸区", "北碚区", "綦江区", "大足区", "渝北区",
        "巴南区", "黔江区", "长寿区", "江津区", "合川区", "永川区",
        "南川区", "璧山区", "铜梁区", "潼南区", "荣昌区", "开州区",
        "梁平区", "武隆区", "城口县", "丰都县", "垫江县", "忠县",
        "云阳县", "奉节县", "巫山县", "巫溪县", "石柱土家族自治县",
        "秀山土家族苗族自治县", "酉阳土家族苗族自治县", "彭水苗族土家族自治县"
    ]
}

async def init_districts_data():
    async with async_session() as session:
        print("开始初始化四个直辖市的区县数据...")
        
        # 获取所有省份
        result = await session.execute(select(Province))
        provinces = result.scalars().all()
        
        # 创建省份名称到ID的映射
        province_map = {province.name: province.id for province in provinces}
        
        total_districts = 0
        
        for province_name, districts in municipality_districts.items():
            if province_name not in province_map:
                print(f"警告: 未找到省份 {province_name}，跳过")
                continue
            
            province_id = province_map[province_name]
            
            # 获取该省份的城市（直辖市通常只有一个城市）
            result = await session.execute(select(City).where(City.province_id == province_id))
            cities = result.scalars().all()
            
            if not cities:
                print(f"警告: 省份 {province_name} 没有找到对应的城市，跳过")
                continue
            
            # 取第一个城市（直辖市的情况）
            city = cities[0]
            
            # 检查该城市是否已经有区县数据
            result = await session.execute(select(District).where(District.city_id == city.id))
            existing_districts = result.scalars().all()
            
            if existing_districts:
                print(f"省份 {province_name} 已有 {len(existing_districts)} 个区县数据，跳过")
                continue
            
            # 添加区县数据
            for district_name in districts:
                district = District(city_id=city.id, name=district_name)
                session.add(district)
                total_districts += 1
            
            print(f"省份 {province_name} 添加了 {len(districts)} 个区县")
        
        await session.commit()
        print(f"区县数据初始化完成！共添加 {total_districts} 个区县")

if __name__ == "__main__":
    asyncio.run(init_districts_data())
