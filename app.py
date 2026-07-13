from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลสถานที่ท่องเที่ยว Mini Tour One Day ในจังหวัดพิษณุโลก
LOCATIONS = [
    {
        "id": 1,
        "name": "Phu Hin Rong Kla National Park",
        "lat": 17.014456721223098,
        "lng": 100.99497236191658,
        "description": "สัมผัสอากาศบริสุทธิ์และร่องรอยประวัติศาสตร์ ณ อุทยานแห่งชาติภูหินร่องกล้า ตื่นตาตื่นใจไปกับลานหินปุ่ม ลานหินแตก และความอุดมสมบูรณ์ของป่าสนบนภูเขาสูง เหมาะสำหรับการเริ่มต้นทริปในยามเช้า",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBTnkd4XnjPPyb2awMmAl5KjA1Ifeh7rNlvPUs9GzisgdJTbMhuu8cvlc&s=10",
        "gmaps_url": "https://www.google.com/maps/dir/?api=1&destination=17.014456721223098,100.99497236191658"
    },
    {
        "id": 2,
        "name": "Namtok Kaeng Sopha",
        "lat": 16.873121549516256,
        "lng": 100.83500376970743,
        "description": "แวะชมความยิ่งใหญ่ของ 'ไนแองการาแห่งเมืองไทย' น้ำตกแก่งโสภา น้ำตกหินปูนขนาดใหญ่ 3 ชั้น ที่มีสายน้ำไหลเชี่ยวผ่านแก่งหินอย่างงดงาม รายล้อมด้วยพรรณไม้ร่มรื่นชวนผ่อนคลาย",
        "image_url": "https://i0.wp.com/chatkeawnice.wordpress.com/wp-content/uploads/2018/11/kaeng-sopha-waterfall.jpg?ssl=1",
        "gmaps_url": "https://www.google.com/maps/dir/?api=1&destination=16.873121549516256,100.83500376970743"
    },
    {
        "id": 3,
        "name": "วัดพระศรีรัตนมหาธาตุวรมหาวิหาร",
        "lat": 16.824173067574506,
        "lng": 100.26192594689871,
        "description": "เดินทางเข้าสู่ตัวเมืองเพื่อกราบนมัสการ 'พระพุทธชินราช' พระพุทธรูปที่ได้รับการยกย่องว่ามีความงดงามที่สุดในประเทศไทย ณ วัดใหญ่ ศูนย์รวมจิตใจของชาวพิษณุโลกและผู้มาเยือนทั่่วโลก",
        "image_url": "https://www.dhammathai.org/watthai/data/imagedb/23-1.jpg",
        "gmaps_url": "https://www.google.com/maps/dir/?api=1&destination=16.824173067574506,100.26192594689871"
    },
    {
        "id": 4,
        "name": "บ้านสวนชมวิว ต้นไม้หัวใจ (Heart Tree House)",
        "lat": 16.732985599697134,
        "lng": 100.62478788046378,
        "description": "พักผ่อนยามบ่าย ณ บ้านรักไทย อำเภอเนินมะปราง ไฮไลต์คือการขึ้นไปชมวิวบนต้นไม้รูปหัวใจที่ยื่นออกไปสัมผัสทิวเขาแบบพาโนรามา บรรยากาศเงียบสงบ ลมเย็นสบาย เหมาะแก่การถ่ายภาพ",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuyTEULS-TRLWB39GIpuE86YdpeQIkptb9DY1vxomqKw&s=10",
        "gmaps_url": "https://www.google.com/maps/dir/?api=1&destination=16.732985599697134,100.62478788046378"
    },
    {
        "id": 5,
        "name": "จุดชมค้างคาว เนินมะปราง",
        "lat": 16.56325560496591,
        "lng": 100.69226827488114,
        "description": "ปิดทริป One Day สุดประทับใจในยามเย็น ณ บ้านมุง ชมปรากฏการณ์ฝูงค้างคาวนับล้านตัวบินออกจากถ้ำหินปูนเป็นสายยาวพาดผ่านท้องฟ้ายามพระอาทิตย์ตกดิน ท่ามกลางบรรยากาศธรรมชาติที่หาชมได้ยาก",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgOVO-Ps1jz9-944TwlNSagziBe2CfPIMBsHLct9tc4YDDm4-gg7IbxvfJ&s=10",
        "gmaps_url": "https://www.google.com/maps/dir/?api=1&destination=16.56325560496591,100.69226827488114"
    }
]

def create_map():
    # ใช้พิกัดกึ่งกลางเฉลี่ยเพื่อเริ่มต้นโฟกัสแผนที่จังหวัดพิษณุโลก
    start_coords = [16.800, 100.650]
    
    # สร้างแผนที่สไตล์คลีน (CartoDB Positron) เพื่อคงความเป็น Minimalist UI
    m = folium.Map(
        location=start_coords, 
        zoom_start=10, 
        tiles="CartoDB positron"
    )
    
    # ดึงพิกัดเพื่อวาดเส้นทางตามลำดับทริป
    route_points = [(loc["lat"], loc["lng"]) for loc in LOCATIONS]
    folium.PolyLine(
        route_points, 
        color="#4a4a4a", 
        weight=3, 
        opacity=0.7,
        dash_array="6, 12"
    ).add_to(m)
    
    # ปักหมุดให้กับทุกสถานที่
    for loc in LOCATIONS:
        popup_html = f"""
        <div style="font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 13px; color: #222; min-width: 180px;">
            <strong style="display:block; margin-bottom: 4px; color: #111;">{loc['name']}</strong>
            <p style="margin: 0 0 8px 0; color: #666; font-size: 11px;">ลำดับที่ {loc['id']} ของทริป</p>
            <a href="{loc['gmaps_url']}" target="_blank" style="display: inline-block; background: #222; color: #fff; padding: 4px 10px; text-decoration: none; font-size: 11px; border-radius: 2px; font-weight: 500;">นำทาง</a>
        </div>
        """
        
        folium.Marker(
            location=[loc["lat"], loc["lng"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"จุดที่ {loc['id']}: {loc['name']}",
            icon=folium.Icon(color="darkred", icon="info-sign")
        ).add_to(m)
        
    return m._repr_html_()

@app.route("/")
def index():
    map_html = create_map()
    
    # สร้างลิงก์รวมเส้นทางทั้งหมดสำหรับปุ่มหลัก Explore Route ด้านล่าง
    origin = f"{LOCATIONS[0]['lat']},{LOCATIONS[0]['lng']}"
    destination = f"{LOCATIONS[-1]['lat']},{LOCATIONS[-1]['lng']}"
    waypoints = "|".join([f"{loc['lat']},{loc['lng']}" for loc in LOCATIONS[1:-1]])
    full_route_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}&travelmode=driving"
    
    return render_template("index.html", locations=LOCATIONS, map_html=map_html, full_route_url=full_route_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
