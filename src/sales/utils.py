import uuid,base64
from customers.models import Customer         #Customer is foreign key to Customers
from profiles.models import Profile           #Salesman is foreign key of Profiles
from io import BytesIO
import matplotlib.pyplot as plt 
import seaborn as sns

def generate_code():
    code = uuid.uuid4()
    code_mod = str(code).replace('-', '').upper()[:12]
    return code_mod

def get_salesman_from_id(value):
    salesman = Profile.objects.get(id=value)
    return salesman.user.username


def get_customer_from_id(value):
    customer = Customer.objects.get(id=value)
    return customer

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph   

def get_key(res_by):
    if res_by == "#1":
        key = "transaction_id"
    elif res_by == "#2":
        key = "created"
    return key

def get_chart(chart_type, data, results_by, **kwargs):
    plt.switch_backend("AGG")      #In jupyter notebook we have inline backend,here we have AGG(Anti Grain Geometry) for writing files,good for rendering PNGs
    fig = plt.figure(figsize =(10,4))
    key = get_key(results_by)
    d = data.groupby(key, as_index=False)['total_price'].agg('sum')
    if chart_type == '#1':
        print("Bar Chart")
        # plt.bar(d[key], d['total_price'])
        sns.barplot(x=key, y='total_price', data=d)
    elif chart_type == '#2':
        print("Pie Chart")
        plt.pie(data = d, x = 'total_price', labels = d[key].values)
    elif chart_type == '#3':
        print("Line Chart")
        plt.plot(d[key], d['total_price'], color='red', marker='o', linestyle='dashed')
    else:
        print("Oopss....Failed to identify Chart Type")

    plt.tight_layout()

    chart = get_graph()
    return chart  