from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)

# 数据库配置：优先使用环境变量（Render PostgreSQL），否则使用 SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Render 提供的 PostgreSQL URL 格式是 postgres://，需要转换为 postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # 本地开发使用 SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///amr_devices.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
db = SQLAlchemy(app)

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 数据库模型
class AMRDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 车端 (Vehicle Terminal)
    vehicle_name = db.Column(db.String(100))
    vehicle_number = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    ip = db.Column(db.String(50))
    status = db.Column(db.String(50))  # 状态
    area = db.Column(db.String(100))  # 区域
    amr_version = db.Column(db.String(50))
    amr_web_version = db.Column(db.String(50))
    amr_system_version = db.Column(db.String(50))
    map_name = db.Column(db.String(100))
    charge_station_name = db.Column(db.String(100))
    transition_point_name = db.Column(db.String(100))
    shelf_name = db.Column(db.String(100))
    machine_work_point_name = db.Column(db.String(100))
    ti_wifi_account = db.Column(db.String(100))
    ti_wifi_password = db.Column(db.String(100))
    driving_speed = db.Column(db.String(50))
    agvweb = db.Column(db.String(200))  # 存储图片路径
    
    # 手臂 (Arm)
    tm_chassis_number = db.Column(db.String(100))
    tm_arm_serial = db.Column(db.String(100))
    tm_handle_serial = db.Column(db.String(100))
    tm_system_version = db.Column(db.String(50))
    arm_project = db.Column(db.String(100))
    arm_process = db.Column(db.String(100))
    arm_model = db.Column(db.String(100))
    arm_speed = db.Column(db.String(50))
    ui_version = db.Column(db.String(50))
    tsc_version = db.Column(db.String(50))
    floor = db.Column(db.String(50))
    go_point_usage = db.Column(db.String(100))
    arm_shelf_name = db.Column(db.String(100))
    
    # TSC
    robot_timeout = db.Column(db.String(50))
    connect_retry = db.Column(db.String(50))
    minimum_charge_time = db.Column(db.String(50))
    below_power = db.Column(db.String(50))
    run_power = db.Column(db.String(50))
    battery_high_level = db.Column(db.String(50))
    into_idle_time = db.Column(db.String(50))
    max_speed = db.Column(db.String(50))
    speed_rotary = db.Column(db.String(50))
    
    # E-Rack
    erack_program_version = db.Column(db.String(50))
    erack_reading_method = db.Column(db.String(50))  # RFID/TAG
    erack_specification = db.Column(db.String(50))  # 3*4 or 3*3
    
    # 充电桩 (Charging Pile)
    charging_pile_spec = db.Column(db.String(50))  # 正充或侧充
    power_supply = db.Column(db.String(100))
    air_source = db.Column(db.String(100))
    power = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'vehicle_name': self.vehicle_name,
            'id': self.id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'vehicle_number': self.vehicle_number,
            'serial_number': self.serial_number,
            'ip': self.ip,
            'status': self.status,
            'area': self.area,
            'amr_version': self.amr_version,
            'amr_web_version': self.amr_web_version,
            'amr_system_version': self.amr_system_version,
            'map_name': self.map_name,
            'charge_station_name': self.charge_station_name,
            'transition_point_name': self.transition_point_name,
            'shelf_name': self.shelf_name,
            'machine_work_point_name': self.machine_work_point_name,
            'ti_wifi_account': self.ti_wifi_account,
            'ti_wifi_password': self.ti_wifi_password,
            'driving_speed': self.driving_speed,
            'agvweb': self.agvweb,
            'tm_chassis_number': self.tm_chassis_number,
            'tm_arm_serial': self.tm_arm_serial,
            'tm_handle_serial': self.tm_handle_serial,
            'tm_system_version': self.tm_system_version,
            'arm_project': self.arm_project,
            'arm_process': self.arm_process,
            'arm_model': self.arm_model,
            'arm_speed': self.arm_speed,
            'ui_version': self.ui_version,
            'tsc_version': self.tsc_version,
            'floor': self.floor,
            'go_point_usage': self.go_point_usage,
            'arm_shelf_name': self.arm_shelf_name,
            'robot_timeout': self.robot_timeout,
            'connect_retry': self.connect_retry,
            'minimum_charge_time': self.minimum_charge_time,
            'below_power': self.below_power,
            'run_power': self.run_power,
            'battery_high_level': self.battery_high_level,
            'into_idle_time': self.into_idle_time,
            'max_speed': self.max_speed,
            'speed_rotary': self.speed_rotary,
            'erack_program_version': self.erack_program_version,
            'erack_reading_method': self.erack_reading_method,
            'erack_specification': self.erack_specification,
            'charging_pile_spec': self.charging_pile_spec,
            'power_supply': self.power_supply,
            'air_source': self.air_source,
            'power': self.power
        }

class DeviceUpdateRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('amr_device.id'), nullable=False)
    update_date = db.Column(db.Date, nullable=False)  # 更新日期（年-月-日）
    update_person = db.Column(db.String(100))  # 更新人
    update_reason = db.Column(db.Text)  # 更新原因
    update_content = db.Column(db.Text, nullable=False)  # 做了什么更新
    seven_day_result = db.Column(db.Text)  # 观察七天后结果
    is_closed = db.Column(db.Boolean, default=False)  # 是否结案
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 关联设备
    device = db.relationship('AMRDevice', backref='update_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_name': self.device.vehicle_name if self.device else None,
            'device_number': self.device.vehicle_number if self.device else None,
            'update_date': self.update_date.strftime('%Y-%m-%d') if self.update_date else None,
            'update_person': self.update_person,
            'update_reason': self.update_reason,
            'update_content': self.update_content,
            'seven_day_result': self.seven_day_result,
            'is_closed': self.is_closed,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/devices', methods=['GET'])
def get_devices():
    devices = AMRDevice.query.order_by(AMRDevice.created_at.asc()).all()
    return jsonify([device.to_dict() for device in devices])

@app.route('/api/devices', methods=['POST'])
def create_device():
    # 处理文件上传
    agvweb_path = None
    if 'agvweb' in request.files:
        file = request.files['agvweb']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 添加时间戳避免文件名冲突
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            agvweb_path = filename
    
    # 获取表单数据
    data = request.form
    device = AMRDevice(
        vehicle_name=data.get('vehicle_name'),
        vehicle_number=data.get('vehicle_number'),
        serial_number=data.get('serial_number'),
        ip=data.get('ip'),
        status=data.get('status'),
        area=data.get('area'),
        amr_version=data.get('amr_version'),
        amr_web_version=data.get('amr_web_version'),
        amr_system_version=data.get('amr_system_version'),
        map_name=data.get('map_name'),
        charge_station_name=data.get('charge_station_name'),
        transition_point_name=data.get('transition_point_name'),
        shelf_name=data.get('shelf_name'),
        machine_work_point_name=data.get('machine_work_point_name'),
        ti_wifi_account=data.get('ti_wifi_account'),
        ti_wifi_password=data.get('ti_wifi_password'),
        driving_speed=data.get('driving_speed'),
        agvweb=agvweb_path,
        tm_chassis_number=data.get('tm_chassis_number'),
        tm_arm_serial=data.get('tm_arm_serial'),
        tm_handle_serial=data.get('tm_handle_serial'),
        tm_system_version=data.get('tm_system_version'),
        arm_project=data.get('arm_project'),
        arm_process=data.get('arm_process'),
        arm_model=data.get('arm_model'),
        arm_speed=data.get('arm_speed'),
        ui_version=data.get('ui_version'),
        tsc_version=data.get('tsc_version'),
        floor=data.get('floor'),
        go_point_usage=data.get('go_point_usage'),
        arm_shelf_name=data.get('arm_shelf_name'),
        robot_timeout=data.get('robot_timeout'),
        connect_retry=data.get('connect_retry'),
        minimum_charge_time=data.get('minimum_charge_time'),
        below_power=data.get('below_power'),
        run_power=data.get('run_power'),
        battery_high_level=data.get('battery_high_level'),
        into_idle_time=data.get('into_idle_time'),
        max_speed=data.get('max_speed'),
        speed_rotary=data.get('speed_rotary'),
        erack_program_version=data.get('erack_program_version'),
        erack_reading_method=data.get('erack_reading_method'),
        erack_specification=data.get('erack_specification'),
        charging_pile_spec=data.get('charging_pile_spec'),
        power_supply=data.get('power_supply'),
        air_source=data.get('air_source'),
        power=data.get('power')
    )
    db.session.add(device)
    db.session.commit()
    return jsonify(device.to_dict()), 201

@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = AMRDevice.query.get_or_404(device_id)
    
    # 处理文件上传
    if 'agvweb' in request.files:
        file = request.files['agvweb']
        if file and file.filename and allowed_file(file.filename):
            # 删除旧文件
            if device.agvweb:
                old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], device.agvweb)
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)
            
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            device.agvweb = filename
    
    # 获取表单数据
    data = request.form
    
    device.vehicle_name = data.get('vehicle_name', device.vehicle_name)
    device.vehicle_number = data.get('vehicle_number', device.vehicle_number)
    device.serial_number = data.get('serial_number', device.serial_number)
    device.ip = data.get('ip', device.ip)
    device.status = data.get('status', device.status)
    device.area = data.get('area', device.area)
    device.amr_version = data.get('amr_version', device.amr_version)
    device.amr_web_version = data.get('amr_web_version', device.amr_web_version)
    device.amr_system_version = data.get('amr_system_version', device.amr_system_version)
    device.map_name = data.get('map_name', device.map_name)
    device.charge_station_name = data.get('charge_station_name', device.charge_station_name)
    device.transition_point_name = data.get('transition_point_name', device.transition_point_name)
    device.shelf_name = data.get('shelf_name', device.shelf_name)
    device.machine_work_point_name = data.get('machine_work_point_name', device.machine_work_point_name)
    device.ti_wifi_account = data.get('ti_wifi_account', device.ti_wifi_account)
    device.ti_wifi_password = data.get('ti_wifi_password', device.ti_wifi_password)
    device.driving_speed = data.get('driving_speed', device.driving_speed)
    device.tm_chassis_number = data.get('tm_chassis_number', device.tm_chassis_number)
    device.tm_arm_serial = data.get('tm_arm_serial', device.tm_arm_serial)
    device.tm_handle_serial = data.get('tm_handle_serial', device.tm_handle_serial)
    device.tm_system_version = data.get('tm_system_version', device.tm_system_version)
    device.arm_project = data.get('arm_project', device.arm_project)
    device.arm_process = data.get('arm_process', device.arm_process)
    device.arm_model = data.get('arm_model', device.arm_model)
    device.arm_speed = data.get('arm_speed', device.arm_speed)
    device.ui_version = data.get('ui_version', device.ui_version)
    device.tsc_version = data.get('tsc_version', device.tsc_version)
    device.floor = data.get('floor', device.floor)
    device.go_point_usage = data.get('go_point_usage', device.go_point_usage)
    device.arm_shelf_name = data.get('arm_shelf_name', device.arm_shelf_name)
    device.robot_timeout = data.get('robot_timeout', device.robot_timeout)
    device.connect_retry = data.get('connect_retry', device.connect_retry)
    device.minimum_charge_time = data.get('minimum_charge_time', device.minimum_charge_time)
    device.below_power = data.get('below_power', device.below_power)
    device.run_power = data.get('run_power', device.run_power)
    device.battery_high_level = data.get('battery_high_level', device.battery_high_level)
    device.into_idle_time = data.get('into_idle_time', device.into_idle_time)
    device.max_speed = data.get('max_speed', device.max_speed)
    device.speed_rotary = data.get('speed_rotary', device.speed_rotary)
    device.erack_program_version = data.get('erack_program_version', device.erack_program_version)
    device.erack_reading_method = data.get('erack_reading_method', device.erack_reading_method)
    device.erack_specification = data.get('erack_specification', device.erack_specification)
    device.charging_pile_spec = data.get('charging_pile_spec', device.charging_pile_spec)
    device.power_supply = data.get('power_supply', device.power_supply)
    device.air_source = data.get('air_source', device.air_source)
    device.power = data.get('power', device.power)
    
    db.session.commit()
    return jsonify(device.to_dict())

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = AMRDevice.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device deleted successfully'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 设备更新记录相关路由
@app.route('/api/update-records', methods=['GET'])
def get_update_records():
    # 按更新日期升序排列，同一日期的按创建时间升序
    records = DeviceUpdateRecord.query.order_by(DeviceUpdateRecord.update_date.asc(), DeviceUpdateRecord.created_at.asc()).all()
    return jsonify([record.to_dict() for record in records])

@app.route('/api/update-records', methods=['POST'])
def create_update_record():
    data = request.json
    try:
        update_date = datetime.strptime(data.get('update_date'), '%Y-%m-%d').date()
    except:
        return jsonify({'error': '日期格式错误'}), 400
    
    record = DeviceUpdateRecord(
        device_id=data.get('device_id'),
        update_date=update_date,
        update_person=data.get('update_person', ''),
        update_reason=data.get('update_reason', ''),
        update_content=data.get('update_content', ''),
        seven_day_result=data.get('seven_day_result', ''),
        is_closed=data.get('is_closed', False)
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

@app.route('/api/update-records/<int:record_id>', methods=['PUT'])
def update_update_record(record_id):
    record = DeviceUpdateRecord.query.get_or_404(record_id)
    data = request.json
    
    if 'update_date' in data:
        try:
            record.update_date = datetime.strptime(data.get('update_date'), '%Y-%m-%d').date()
        except:
            return jsonify({'error': '日期格式错误'}), 400
    
    if 'device_id' in data:
        record.device_id = data.get('device_id')
    if 'update_person' in data:
        record.update_person = data.get('update_person', '')
    if 'update_reason' in data:
        record.update_reason = data.get('update_reason', '')
    if 'update_content' in data:
        record.update_content = data.get('update_content', '')
    if 'seven_day_result' in data:
        record.seven_day_result = data.get('seven_day_result', '')
    if 'is_closed' in data:
        record.is_closed = data.get('is_closed', False)
    
    db.session.commit()
    return jsonify(record.to_dict())

@app.route('/api/update-records/<int:record_id>', methods=['DELETE'])
def delete_update_record(record_id):
    record = DeviceUpdateRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Update record deleted successfully'})

# 初始化数据库表
with app.app_context():
    db.create_all()

# 本地开发时运行
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

