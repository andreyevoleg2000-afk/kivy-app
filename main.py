from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window
import math

# --- ФИЗИЧЕСКИЕ КОНСТАНТЫ (СИ) ---
G = 6.67430e-11
C = 299792458
AU = 1.495978707e11
SIGMA = 5.670374419e-8  # Постоянная Стефана-Больцмана
L_SUN_WATTS = 3.828e26  # Мощность излучения Солнца в Ваттах

# Массы в кг
M_MOON = 7.342e22
M_EARTH = 5.9722e24
M_JUPITER = 1.8982e27
M_SUN = 1.9891e30

# Радиусы в метрах
R_MOON = 1737400
R_EARTH = 6371000
R_JUPITER = 69911000
R_SUN = 696340000

Window.clearcolor = (0.03, 0.03, 0.05, 1)

class InputRow(BoxLayout):
    label_text = StringProperty('')
    unit_type = StringProperty('none')
    spinner_values = ListProperty([])

    def on_unit_type(self, instance, value):
        units = {
            'mass': ['M_Земли', 'M_Юпитера', 'M_Солнца', 'M_Луны'],
            'length': ['км', 'R_Земли', 'R_Юпитера', 'R_Солнца', 'R_Луны', 'м'],
            'density': ['г/см³', 'кг/м³'],
            'temp': ['Кельвины'],
            'lum': ['L_Солнца']
        }
        self.spinner_values = units.get(value, ['ед.'])
        if self.spinner_values:
            self.ids.unit_spinner.text = self.spinner_values[0]

    def get_value_si(self):
        text = self.ids.input_field.text.strip()
        if not text:
            return None  # Возвращаем None, если поле не заполнено (для опциональных полей)
        val = float(text)
        unit = self.ids.unit_spinner.text

        if unit == 'M_Земли': return val * M_EARTH
        if unit == 'M_Юпитера': return val * M_JUPITER
        if unit == 'M_Солнца': return val * M_SUN
        if unit == 'M_Луны': return val * M_MOON
        
        if unit == 'км': return val * 1000.0
        if unit == 'м': return val
        if unit == 'R_Земли': return val * R_EARTH
        if unit == 'R_Юпитера': return val * R_JUPITER
        if unit == 'R_Солнца': return val * R_SUN
        if unit == 'R_Луны': return val * R_MOON
        
        if unit == 'г/см³': return val * 1000.0
        if unit == 'кг/м³': return val
        
        return val

# --- УМНОЕ ФОРМАТИРОВАНИЕ ВЫВОДА ---
def format_mass_output(mass_kg):
    val_moons = mass_kg / M_MOON
    if val_moons <= 87.0: return f"{val_moons:.4f} Лун"
    val_earths = mass_kg / M_EARTH
    if mass_kg <= M_JUPITER: return f"{val_earths:.4f} Земли"
    val_jupiters = mass_kg / M_JUPITER
    if mass_kg <= M_SUN: return f"{val_jupiters:.4f} Юпитеров"
    return f"{mass_kg / M_SUN:.4f} Солнц"

def format_size_output(size_m):
    km_val = size_m / 1000.0
    val_moons = size_m / R_MOON
    if val_moons <= 87.0: return f"{km_val:.2f} км ({val_moons:.4f} R_Луны)"
    val_earths = size_m / R_EARTH
    if size_m <= R_JUPITER: return f"{km_val:.2f} км ({val_earths:.4f} R_Земли)"
    val_jupiters = size_m / R_JUPITER
    if size_m <= R_SUN: return f"{km_val:.2f} км ({val_jupiters:.4f} R_Юпитера)"
    return f"{km_val:.2f} км ({size_m / R_SUN:.4f} R_Солнца)"

KV = '''
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        Label:
            text: 'OMEGA ASTRO-ENGINE Pro'
            font_size: '24sp'
            bold: True
            size_hint_y: 0.15
            color: (0.2, 0.6, 1, 1)
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                spacing: 8
                size_hint_y: None
                height: self.minimum_height
                Button:
                    text: '1. Зона обитаемости (Kopparapu)'
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.manager.current = 'hab_zone'
                Button:
                    text: '2. Орбитальная скорость'
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.manager.current = 'velocity'
                Button:
                    text: '3. Сфера влияния (ОТО Хилл / SOI)'
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.manager.current = 'soi'
                Button:
                    text: '4. Расчёт массы (По Rho и R)'
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.manager.current = 'mass_calc'
                Button:
                    text: '5. Расчёт радиуса (По M и Rho)'
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.manager.current = 'radius_calc'
                Button:
                    text: '6. Расчёт плотности (По M и R)'
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.manager.current = 'density_calc'
                Button:
                    text: '7. Предел Роша'
                    size_hint_y: None
                    height: '48dp'
                    on_release: root.manager.current = 'roche'

<InputRow>:
    orientation: 'horizontal'
    size_hint_y: None
    height: '40dp'
    spacing: 5
    Label:
        text: root.label_text
        text_size: self.size
        halign: 'left'
        valign: 'middle'
        font_size: '13sp'
        size_hint_x: 0.45
    TextInput:
        id: input_field
        multiline: False
        input_filter: 'float'
        size_hint_x: 0.3
        background_color: (0.1, 0.1, 0.15, 1)
        foreground_color: (1, 1, 1, 1)
    Spinner:
        id: unit_spinner
        text: 'загрузка...'
        values: root.spinner_values
        size_hint_x: 0.25

# --- СТРУКТУРА ЭКРАНОВ ---
<HabZoneScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 8
        Label:
            text: 'Зона обитаемости звездных систем'
            font_size: '18sp'
            size_hint_y: 0.08
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                spacing: 8
                size_hint_y: None
                height: self.minimum_height
                InputRow:
                    id: hz_lum
                    label_text: 'Светимость (оставь пустым для авторасчёта):'
                    unit_type: 'lum'
                InputRow:
                    id: hz_temp
                    label_text: 'Температура звезды (обязательно):'
                    unit_type: 'temp'
                InputRow:
                    id: hz_rad
                    label_text: 'Радиус звезды (для авторасчёта L):'
                    unit_type: 'length'
        Button:
            text: 'РАССЧИТАТЬ ГРАНИЦЫ HZ'
            size_hint_y: 0.1
            on_release: root.calculate()
        Label:
            id: result_label
            text: 'Введите параметры родительской звезды'
            size_hint_y: 0.22
            font_size: '13sp'
        Button:
            text: 'В ГЛАВНОЕ МЕНЮ'
            size_hint_y: 0.08
            on_release: root.manager.current = 'menu'

<VelocityScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        Label:
            text: 'Орбитальная скорость'
            font_size: '18sp'
            size_hint_y: 0.08
        InputRow:
            id: v_mass
            label_text: 'Масса родит. тела:'
            unit_type: 'mass'
        InputRow:
            id: v_dens
            label_text: 'Плотность родит. тела:'
            unit_type: 'density'
        InputRow:
            id: v_rad
            label_text: 'Радиус родит. тела:'
            unit_type: 'length'
        InputRow:
            id: v_dist
            label_text: 'Расстояние до центра тел:'
            unit_type: 'length'
        Button:
            text: 'ВЫЧИСЛИТЬ СКОРОСТЬ'
            size_hint_y: 0.12
            on_release: root.calculate()
        Label:
            id: result_label
            text: 'Результаты'
            size_hint_y: 0.2
        Button:
            text: 'В МЕНЮ'
            size_hint_y: 0.08
            on_release: root.manager.current = 'menu'

<SOIScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 8
        Label:
            text: 'Гравитационная сфера влияния'
            font_size: '18sp'
            size_hint_y: 0.08
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                spacing: 8
                size_hint_y: None
                height: self.minimum_height
                InputRow:
                    id: soi_m_obj
                    label_text: 'Масса объекта:'
                    unit_type: 'mass'
                InputRow:
                    id: soi_d_obj
                    label_text: 'Плотность объекта:'
                    unit_type: 'density'
                InputRow:
                    id: soi_r_obj
                    label_text: 'Радиус объекта:'
                    unit_type: 'length'
                InputRow:
                    id: soi_m_par
                    label_text: 'Масса родит. тела:'
                    unit_type: 'mass'
                InputRow:
                    id: soi_d_par
                    label_text: 'Плотность родит. тела:'
                    unit_type: 'density'
                InputRow:
                    id: soi_r_par
                    label_text: 'Радиус родит. тела:'
                    unit_type: 'length'
                InputRow:
                    id: soi_dist
                    label_text: 'Расстояние между ними:'
                    unit_type: 'length'
        Button:
            text: 'ВЫЧИСЛИТЬ ПО ОТО ЭЙНШТЕЙНА'
            size_hint_y: 0.1
            on_release: root.calculate()
        Label:
            id: result_label
            text: 'Ожидание параметров системы...'
            size_hint_y: 0.2
            font_size: '12sp'
        Button:
            text: 'В МЕНЮ'
            size_hint_y: 0.08
            on_release: root.manager.current = 'menu'

<MassScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        Label:
            text: 'Вычисление Массы Объекта'
            font_size: '18sp'
            size_hint_y: 0.08
        InputRow:
            id: m_dens
            label_text: 'Плотность объекта:'
            unit_type: 'density'
        InputRow:
            id: m_rad
            label_text: 'Радиус объекта:'
            unit_type: 'length'
        Button:
            text: 'РАССЧИТАТЬ МАССУ'
            size_hint_y: 0.12
            on_release: root.calculate()
        Label:
            id: result_label
            text: 'Результат'
            size_hint_y: 0.2
        Button:
            text: 'В МЕНЮ'
            size_hint_y: 0.08
            on_release: root.manager.current = 'menu'

<RadiusScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        Label:
            text: 'Вычисление Радиуса Объекта'
            font_size: '18sp'
            size_hint_y: 0.08
        InputRow:
            id: r_mass
            label_text: 'Масса объекта:'
            unit_type: 'mass'
        InputRow:
            id: r_dens
            label_text: 'Плотность объекта:'
            unit_type: 'density'
        Button:
            text: 'РАССЧИТАТЬ РАДИУС'
            size_hint_y: 0.12
            on_release: root.calculate()
        Label:
            id: result_label
            text: 'Результат'
            size_hint_y: 0.2
        Button:
            text: 'В МЕНЮ'
            size_hint_y: 0.08
            on_release: root.manager.current = 'menu'

<DensityScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        Label:
            text: 'Вычисление Плотности Объекта'
            font_size: '18sp'
            size_hint_y: 0.08
        InputRow:
            id: d_mass
            label_text: 'Масса объекта:'
            unit_type: 'mass'
        InputRow:
            id: d_rad
            label_text: 'Радиус объекта:'
            unit_type: 'length'
        Button:
            text: 'РАССЧИТАТЬ ПЛОТНОСТЬ'
            size_hint_y: 0.12
            on_release: root.calculate()
        Label:
            id: result_label
            text: 'Результат'
            size_hint_y: 0.2
        Button:
            text: 'В МЕНЮ'
            size_hint_y: 0.08
            on_release: root.manager.current = 'menu'

<RocheScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        Label:
            text: 'Предел разрушения Роша'
            font_size: '18sp'
            size_hint_y: 0.08
        InputRow:
            id: roche_rad_par
            label_text: 'Радиус родит. тела:'
            unit_type: 'length'
        InputRow:
            id: roche_dens_par
            label_text: 'Плотность родит. тела:'
            unit_type: 'density'
        InputRow:
            id: roche_dens_sat
            label_text: 'Плотность спутника:'
            unit_type: 'density'
        Button:
            text: 'РАССЧИТАТЬ ТРИГГЕР'
            size_hint_y: 0.12
            on_release: root.calculate()
        Label:
            id: result_label
            text: 'Результаты'
            size_hint_y: 0.2
        Button:
            text: 'В МЕНЮ'
            size_hint_y: 0.08
            on_release: root.manager.current = 'menu'
'''

class MenuScreen(Screen): pass

class HabZoneScreen(Screen):
    def calculate(self):
        try:
            lum_text = self.ids.hz_lum.ids.input_field.text.strip()
            t_eff = self.ids.hz_temp.get_value_si()
            
            if not t_eff:
                raise ValueError("Температура звезды обязательна для расчёта!")

            # Умное переключение: если светимость не задана, считаем через Стефана-Больцмана
            if lum_text:
                l_val = float(lum_text)
            else:
                r_m = self.ids.hz_rad.get_value_si()
                if not r_m:
                    raise ValueError("Укажите либо Светимость напрямую, либо Радиус + Температуру!")
                
                # Поток энергии Вт = 4 * pi * R^2 * sigma * T^4
                l_watts = 4 * math.pi * (r_m ** 2) * SIGMA * (t_eff ** 4)
                l_val = l_watts / L_SUN_WATTS
                # Записываем результат обратно в UI для наглядности
                self.ids.hz_lum.ids.input_field.text = f"{l_val:.4f}"

            # Формулы Kopparapu
            t_star = t_eff - 5780.0
            s_eff_in = 1.107 + 1.332e-4 * t_star + 1.580e-8 * (t_star**2) - 8.308e-12 * (t_star**3)
            s_eff_out = 0.356 + 6.171e-5 * t_star + 1.698e-9 * (t_star**2) - 3.198e-12 * (t_star**3)
            
            d_in_au = math.sqrt(l_val / s_eff_in)
            d_out_au = math.sqrt(l_val / s_eff_out)
            
            r_in_m = d_in_au * AU
            r_out_m = d_out_au * AU
            
            self.ids.result_label.text = (
                f"Используемая светимость: {l_val:.4f} L_Солнца\n\n"
                f"Внутренняя граница (Runaway Greenhouse):\n{format_size_output(r_in_m)} [{d_in_au:.4f} А.Е.]\n\n"
                f"Внешняя граница (Maximum Greenhouse):\n{format_size_output(r_out_m)} [{d_out_au:.4f} А.Е.]"
            )
        except Exception as e:
            self.ids.result_label.text = f"Ошибка:\n{str(e)}"

# --- ОСТАЛЬНЫЕ ЭКРАНЫ (БЕЗ ИЗМЕНЕНИЙ) ---
class VelocityScreen(Screen):
    def calculate(self):
        try:
            m_parent = self.ids.v_mass.get_value_si()
            r_orbit = self.ids.v_dist.get_value_si()
            v = math.sqrt((G * m_parent) / r_orbit)
            self.ids.result_label.text = f"Вторая космическая (побег): {v * math.sqrt(2) / 1000.0:.3f} км/с\n" \
                                         f"Орбитальная скорость: {v / 1000.0:.3f} км/с\n" \
                                         f"({v * 3.6:.1f} км/ч)"
        except Exception as e: self.ids.result_label.text = f"Ошибка: {str(e)}"

class SOIScreen(Screen):
    def calculate(self):
        try:
            m_obj = self.ids.soi_m_obj.get_value_si()
            m_parent = self.ids.soi_m_par.get_value_si()
            dist = self.ids.soi_dist.get_value_si()
            r_schwarzschild = (2.0 * G * m_parent) / (C**2)
            oto_factor = 1.0 - (r_schwarzschild / dist)
            r_hill = dist * ((m_obj / (3.0 * m_parent)) ** (1.0 / 3.0)) * oto_factor
            r_soi = dist * ((m_obj / m_parent) ** (0.4))
            self.ids.result_label.text = f"Релятивистский Хилл (ОТО 1PN):\n{format_size_output(r_hill)}\n\n" \
                                         f"Сфера влияния Лапласа (SOI):\n{format_size_output(r_soi)}"
        except Exception as e: self.ids.result_label.text = f"Ошибка: {str(e)}"

class MassScreen(Screen):
    def calculate(self):
        try:
            dens = self.ids.m_dens.get_value_si()
            rad = self.ids.m_rad.get_value_si()
            volume = (4.0 / 3.0) * math.pi * (rad ** 3)
            mass = dens * volume
            self.ids.result_label.text = f"Точная Масса объекта:\n{format_mass_output(mass)}"
        except Exception as e: self.ids.result_label.text = f"Ошибка: {str(e)}"

class RadiusScreen(Screen):
    def calculate(self):
        try:
            mass = self.ids.r_mass.get_value_si()
            dens = self.ids.r_dens.get_value_si()
            rad = ((3.0 * mass) / (4.0 * math.pi * dens)) ** (1.0 / 3.0)
            self.ids.result_label.text = f"Точный Радиус объекта:\n{format_size_output(rad)}"
        except Exception as e: self.ids.result_label.text = f"Ошибка: {str(e)}"

class DensityScreen(Screen):
    def calculate(self):
        try:
            mass = self.ids.d_mass.get_value_si()
            rad = self.ids.d_rad.get_value_si()
            volume = (4.0 / 3.0) * math.pi * (rad ** 3)
            dens = mass / volume
            self.ids.result_label.text = f"Средняя плотность структуры:\n{dens / 1000.0:.4f} г/см³\n({dens:.2f} кг/м³)"
        except Exception as e: self.ids.result_label.text = f"Ошибка: {str(e)}"

class RocheScreen(Screen):
    def calculate(self):
        try:
            r_par = self.ids.roche_rad_par.get_value_si()
            d_par = self.ids.roche_dens_par.get_value_si()
            d_sat = self.ids.roche_dens_sat.get_value_si()
            roche_fluid = 2.423 * r_par * ((d_par / d_sat) ** (1.0 / 3.0))
            roche_rigid = 1.26 * r_par * ((d_par / d_sat) ** (1.0 / 3.0))
            self.ids.result_label.text = f"Жидкостный предел Роша:\n{format_size_output(roche_fluid)}\n\n" \
                                         f"Жёсткий предел Роша:\n{format_size_output(roche_rigid)}"
        except Exception as e: self.ids.result_label.text = f"Ошибка: {str(e)}"

class AstroApp(App):
    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(HabZoneScreen(name='hab_zone'))
        sm.add_widget(VelocityScreen(name='velocity'))
        sm.add_widget(SOIScreen(name='soi'))
        sm.add_widget(MassScreen(name='mass_calc'))
        sm.add_widget(RadiusScreen(name='radius_calc'))
        sm.add_widget(DensityScreen(name='density_calc'))
        sm.add_widget(RocheScreen(name='roche'))
        return sm

if __name__ == '__main__':
    AstroApp().run()
