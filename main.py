# %%
# |exporti
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sps
import streamlit as st
import streamlit as st

from streamlit_jupyter import StreamlitPatcher

StreamlitPatcher().jupyter()


# %%
from nbdev.export import nb_export

nb_export("Гизатуллин_Тимур_Младший_исследователь_данных(DS).ipynb", lib_path="./", name="app")


# %%
# |exporti
st.title("Тестовое задание. Гизатуллин Тимур")
st.header("Описание задачи")
st.markdown("""Суть задания заключается в проверке двух гипотез:
1) Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин.
2) Работники старше 35 лет (age) пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.

по данным о количестве больничных дней для каждого сотрудника с указанием его возраста и пола за последний год(предположительно).""")


# %%
# |exporti
st.markdown("""Гипотезы можно переформулировать так:

$$1. \mu([Male > 2]) \gg \mu([Female > 2])$$

$$2. \mu([Elder > 2]) \gg \mu([Younger > 2])$$""")


# %%
# |exporti
st.markdown("""Гипотезы будем проверять с уровнем значимости = 0.05""")


# %%
# |exporti
uploaded_file = st.file_uploader(label='Выберите файл для загрузки', type = ["csv"])
    # Форма для загрузки изображения средствами Streamlit
if uploaded_file is not None:
        # Получение загруженного файла
    data = pd.read_csv(uploaded_file, encoding='latin-1', sep = ",")
        # Показ загруженного файла на Web-странице средствами Streamlit
    st.dataframe(data)
        # Возврат файла в формате .csv


# %%
show_data = st.sidebar.checkbox('Show raw data')
if show_data == True:
    st.subheader('Raw data')
    st.write(data)


# %%
# |exporti
st.markdown("Как видим, в силу некорректной кодировки, а также неправильного формата разделения: все значения содержатся в одном столбце, нам придется провести некоторые модификации с датафреймом")


# %%
# |exporti
data = data[data.columns[0]].str.split(",", expand = True)
data.columns = ["sick_days_amount", 'age', 'sex']
data['sex'] = np.where((data['sex'] == data['sex'][0]), "female", "male") # тут узнал что есть М, а что - Ж по обратной кодировке
data['age'], data['sick_days_amount'] = data['age'].astype('int'), data['sick_days_amount'].astype('int')
st.dataframe(data)


# %%
# |exporti
print(data.info(), data.describe())


# %%
# |exporti
print(data.isnull().sum().sum()) # в датафрейме нет пропущенных значений


# %%
# |exporti
st.markdown("Все готово! Пусть и с костылями(вполне возможно банально в силу моей прошивки у меня все работает иначе, чем должно), теперь данные в готовом, правильном виде")


# %%
# |exporti
st.markdown("Посмотрим, присутствует ли дизбаланс классов:")


# %%
# |exporti
fig, ax = plt.subplots(figsize = (10, 6), ncols = 2)
ax[0].pie([(data['sex'] == 'female').sum(), (data['sex'] == 'male').sum()], labels = ['female', 'male'], autopct = "%1.2f%%")
ax[1].pie([(data['age'] > 35).sum(), (data['age'] <= 35).sum()], labels = ['employees older than 35', 'employees younger than 35'], autopct = "%1.2f%%")
st.pyplot(fig)


# %%
# |exporti
st.markdown("Он присутствует, но в силу того, что мы не будем работать с методами, которые плохо работают с несбалансированными классами при проверке гипотез, просто будем иметь в виду, что по-хорошему нужно брать в расчет, что при экстраполяции рассуждений про возраст сотрудников, стоит вспомнить о дисбалансе классов в данной работе")


# %%
# |exporti
st.markdown("Сохраним в отдельные переменные интересующие нас серии - сотрудников мужчин/женщин, и сотрудников старше 35 лет/не старше 35 лет")


# %%
# |exporti
male = data['sick_days_amount'][data['sex'] == 'male']
female = data['sick_days_amount'][data['sex'] == 'female']
elder = data['sick_days_amount'][data['age'] > 35]
younger = data['sick_days_amount'][data['age'] <= 35]
male.name, female.name, elder.name, younger.name = "Male", "Female", "Elder", "Younger"


# %%
# |exporti
st.markdown("Посмотрим на распределения количества больничных дней людей разного пола и разного возраста:")


# %%
# |exporti
fig, ax = plt.subplots(ncols = 2, figsize = (20, 10))
fig.set(facecolor = '#eee')
x = np.arange(0, 9, 1)
w = 0.35
sick_days_male = np.array([(male == i).sum() for i in x])
sick_days_female = np.array([(female == i).sum() for i in x])
sick_days_elder = np.array([(elder == i).sum() for i in x])
sick_days_younger = np.array([(younger == i).sum() for i in x])
ax[0].bar(x - w / 2, sick_days_male, label = "Male", width = w)
ax[0].bar(x + w / 2, sick_days_female, label = "Female", width = w)
ax[1].bar(x - w / 2, sick_days_elder, label = "Elder", width = w)
ax[1].bar(x + w / 2, sick_days_younger, label = "Younger", width = w)
ax[0].grid(which = 'major', color = '#444', lw = 0.1)
ax[1].grid(which = 'major', color = '#444', lw = 0.1)
ax[0].set_xticks(x), ax[1].set_xticks(x)
ax[0].set_title('Distribution of employees based on their sex'), ax[1].set_title('Distribution of employees based on their age')
ax[0].set_ylabel('Amount of employees'), ax[1].set_ylabel('Amount of employees')
ax[0].set_xlabel('Amount of sick days'), ax[1].set_xlabel('Amount of sick days')
ax[0].legend(), ax[1].legend()
st.pyplot(fig)


# %%
# |exporti
fig, ax = plt.subplots(ncols = 2, figsize = (20, 10))
fig.set(facecolor = '#eee')
x = np.arange(0, 9, 1)
x_1 = np.arange(0, 9, 0.1)
ax[0].hist(male, density = True, color = "red", label = "Male", alpha = 0.3, bins = 9)
ax[0].hist(female, density = True, color = "blue", label = "Female", alpha = 0.3, bins = 9)
ax[0].plot(x_1, sps.norm(male.mean(), male.std()).pdf(x_1), color = "red", label = "Male")
ax[0].plot(x_1, sps.norm(female.mean(), female.std()).pdf(x_1), color = "blue", label = "Female")
ax[1].hist(elder, density = True, color = "red", label = "Elder", alpha = 0.3, bins = 9)
ax[1].hist(younger, density = True, color = "blue", label = "Younger", alpha = 0.3, bins = 9)
ax[1].plot(x_1, sps.norm(elder.mean(), elder.std()).pdf(x_1), color = "red", label = "Elder")
ax[1].plot(x_1, sps.norm(younger.mean(), younger.std()).pdf(x_1), color = "blue", label = "Younger")
ax[0].grid(which = 'major', color = '#444', lw = 0.1)
ax[1].grid(which = 'major', color = '#444', lw = 0.1)
ax[0].set_xticks(x), ax[1].set_xticks(x)
ax[0].set_title('Histogram of employees based on their sex'), ax[1].set_title('Histogram of employees based on their age')
ax[0].set_ylabel('Amount of employees'), ax[1].set_ylabel('Amount of employees')
ax[0].set_xlabel('Amount of sick days'), ax[1].set_xlabel('Amount of sick days')
ax[0].legend(), ax[1].legend()
st.pyplot(fig)


# %%
fig, ax = plt.subplots(ncols = 2, figsize = (20, 10))
fig.set(facecolor = '#eee')
x = np.arange(3, 9, 1)
x_1 = np.arange(3, 9, 0.1)
ax[0].hist(male[male > 2], density = True, color = "red", label = "Male", alpha = 0.3)
ax[0].hist(female[female > 2], density = True, color = "blue", label = "Female", alpha = 0.3)
ax[0].plot(x_1, sps.norm(male[male > 2].mean(), male[male > 2].std()).pdf(x_1), color = "red", label = "Male")
ax[0].plot(x_1, sps.norm(female[female > 2].mean(), female[female > 2].std()).pdf(x_1), color = "blue", label = "Female")
ax[1].hist(elder[elder > 2], density = True, color = "red", label = "Elder", alpha = 0.3, bins = 9)
ax[1].hist(younger[younger > 2], density = True, color = "blue", label = "Younger", alpha = 0.3, bins = 9)
ax[1].plot(x_1, sps.norm(elder[elder > 2].mean(), elder[elder > 2].std()).pdf(x_1), color = "red", label = "Elder")
ax[1].plot(x_1, sps.norm(younger[younger > 2].mean(), younger[younger > 2].std()).pdf(x_1), color = "blue", label = "Younger")
ax[0].grid(which = 'major', color = '#444', lw = 0.1)
ax[1].grid(which = 'major', color = '#444', lw = 0.1)
ax[0].set_xticks(x), ax[1].set_xticks(x)
ax[0].set_title('Histogram of employees based on their sex'), ax[1].set_title('Histogram of employees based on their age')
ax[0].set_ylabel('Amount of employees'), ax[1].set_ylabel('Amount of employees')
ax[0].set_xlabel('Amount of sick days'), ax[1].set_xlabel('Amount of sick days')
ax[0].legend(), ax[1].legend()
st.pyplot(fig)


# %%
fig = plt.figure()
sns.displot(male, kde = True, bins = 9, stat = "percent", label = "Male")
plt.legend()
st.pyplot(fig)


# %%
fig = plt.figure()
sns.displot(female, kde = True, bins = 9, stat = "percent", label = "Female")
plt.legend()
st.pyplot(fig)


# %%
fig = plt.figure()
sns.displot(elder, kde = True, bins = 9, stat = "percent", label = "Elder")
plt.legend()
st.pyplot(fig)


# %%
fig = plt.figure()
sns.displot(younger, kde = True, bins = 9, stat = "percent", label = "Younger")
plt.legend()
st.pyplot(fig)


# %%
# |exporti
st.markdown("""Проверим, равны ли дисперсии с помощью критерия Флигнера-Килина:

p-value for male/female: 0.521300054528677

p-value for elder/younger: 0.577429487644749""")

st.header("Уже на этом моменте можно сделать промежуточные выводы: визуально гипотезы отвергаются: среднее ни по всем дням, ни по дням, заведомо большим 2, ни у мужчин, ни у сотрудников старше 35, не значительно больше, чем у женщин и сотрудников младше 45 соответсвенно")

st.markdown("Как видим, распределения всех подвыборок условно нормальны.")


# %%
# |exporti
st.markdown("С предположением нормальности распределений посчитаем коэффиценты асимметричности и коэффиценты эксцесса для каждой подвыборки:")


# %%
# |exporti
st.markdown("""skew for male: 0.6067065891837976

skew for female: 0.39155159923496313

skew for elder: 0.49496297808182604

skew for younger: 0.566980016696773

kurtosis for male: 0.06505299465667269

kurtosis for female: -0.3128281110063993

kurtosis for elder: -0.08896906917026026

kurtosis for younger: -0.022074744077901443

Все подвыборки(опять же, в предположении их визуальной условной нормальности) оказываются положительно асимметричными нормальными.

И проведем тест критерием асимметричности и эксцесса:

p-value for male: 0.004241974397249691

p-value for female: 0.1014452240311182

p-value for elder: 0.0073590623737652735

p-value for younger: 0.06675296318279056""")


# %%
# |exporti
st.markdown("""p-value недостатчно большой, в силу чего у нас есть достаточно оснований для отвержения гипотезы о нормальности наших выборок.

Подтверждается, что они принадлежат параметрическому семейству распределений, критерием согласия Пирсона:

p-value for male: 0.15452086628661144

p-value for female: 0.8585814797449028

p-value for elder: 0.5390945133682639

p-value for younger: 0.333555647083237

Попробуем проверить принадлежность наших подвыборок к какому-либо семейству распределений из возможных на вид с помощью t-теста Стьюдента:""")


# %%
# |exporti
st.markdown("""Ни одно из опробованных распределений не оказалось подтверждено, разве что гамма-распределение давало неплохие относительные значения p-value. Другими словами, найти правильное оригинальное распределение у меня не получилось.

Далее я пытался подобрать параметр гамма-распределения, при котором будет достигаться максимальное значение функции правдоподобия, но это не увенчалось успехом, потому что, как мне кажется, на этом моменте я уже шел не в ту сторону, ведь для проверки основных гипотез у нас уже есть все, что нужно:""")


# %%
# |exporti
st.markdown("""В распределениях нет выбросов, которые не дают применить критерий Стьюдента, а также размер наших выборок достаточно большой, чтобы не требовать оговорку на их нормальность при тесте Стьюдента.

На гистограммах для полов и мужское, и женское распределения условно нормальны. Их дисперсии, в силу достаточно большого p-value по критерию Флингера-Килина, с допущением на ошибку равны.

Для распределений для полов и для возрастов в четырех выборках попарно находятся разные наблюдаемые обьекты, то есть выборки несвязные. Значит, гипотезу о равенстве средних будем проверять с помощью t-теста Стьюдента:

p-value for male/female: 0.67806332103283

p-value for elder/younger: 0.4487922957971878

Значит, обе первоначальных гипотезы мы отвергаем - средние значения не удовлетворяют условию о значительно большем среднем.""")

st.header("Вывод: итак, в ходе работы был проведен анализ датасета количества в течение года больничных дней людей - мужчин и женщин, людей старше 35 и нет, и были отпровергнуты обе первоначальные гипотезы:")

st.markdown("""1) Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин.

2) Работники старше 35 лет (age) пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.""")
