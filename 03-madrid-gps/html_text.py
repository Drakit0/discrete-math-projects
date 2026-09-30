# html de la página web que se renderiza con flask

html_text = """
<!DOCTYPE html>
<html lang="en">
    <head>
        {{header|safe}}
        <style>
            form{
                position: absolute;
                z-index: 999;
                background-color:white;
                width: 100%;
            }
            .direcciones{
                display:flex;
                position:absolute;
                width:25%;
                top:10%;
                z-index:400;                
                background-color:white;
                padding:0;
                height: 87vh;
                overflow-y: hidden;
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                flex-direction: column;
                                    
            .directions{
                display: inline-block;
                width: 100%;
                overflow-y:scroll;
            }

            }
            .distancias{
                left:49%;                
            }
            .velocidades{
                left:75%;
            }
            p{
                border-width: 1px 0 0 0;
                border-style: solid;
                margin: 0;
                padding: 5px;
            }
            .title{
                border: 0;
                box-shadow: 0 0 4px 0 rgba(0, 0, 0, 0.2);
            }

            .option{
                width: 45%;
                display: inline-block;
                padding: 5px 0px 2px 10px;
            }
            .leyenda{
                position:absolute;
                z-index: 999;
                top: 10%;
                left: 33%;
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                background-color:white;
            }
            .leyenda p{
                border-width: 0;
            }
            span:after {
                content: "";
                display: inline-block;
                width: 15px;
                height: 15px;
                margin-left: 5px;
                margin-right: 10px;
                transform: translateY(15%)

                }
            .blue:after{
                background: Blue;
            }
            .green:after{
                background: green;
            }
            .alert{
                position:absolute;
                top: 50%;
                left: 50%;
                background-color: #e01e37;
                color: #641220;
                z-index:999;
                width: 60%;
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                transform: translate(-50%, -50%);
                text-align:center;
            }
            .alert p{
                border-width: 0;
            }
            button{
                position:relative;
                {% if selected_calle_salida or selected_calle_llegada %}
                top: 2vh;
                {% endif %}
                border: 1px solid;
                border-radius: 5px;
                transition: 300ms;
            }
            button:hover{
                box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 3px 10px 0 rgba(0, 0, 0, 0.14);
            }
            
        </style>
    </head>
    <body>
        <form method = "get" autocomplete="off">
            <div class='option'>
                <label for="input">Seleccione calle de salida:</label>
                {% if selected_calle_salida %}
                    <input name = "calles_salida_input" type="text" list="calles_salida" value = "{{selected_calle_salida}}"/>
                {% else %}
                    <input name = "calles_salida_input" type="text" list="calles_salida"/>
                {% endif %}
                <datalist id="calles_salida">
                    {% for name in names %}
                    <option value="{{name}}">{{name}}</option>
                    {% endfor %}
                </datalist>
            </div>
            <div class='option'>
                <label for="input">Seleccione calle de llegada:</label>
                {% if selected_calle_llegada %}
                    <input name = "calles_llegada_input" type="text" list="calles_llegada" value = "{{selected_calle_llegada}}"/>
                {% else %}
                    <input name = "calles_llegada_input" type="text" list="calles_llegada"/>
                {% endif %}
                <datalist id="calles_llegada">
                    {% for name in names %}
                    <option value="{{name}}">{{name}}</option>
                    {% endfor %}
                </datalist>
            </div>
            <button type = "submit">Submit</button>

            <br>

            <div class = 'option'>
                {% if selected_calle_salida %}

                    <label for="input">Seleccione número de portal o calle que cruza a calle de salida:</label>
                    {% if selected_calle_cruza_salida %}
                        <input name = "calle_cruza_salida" type="text" list="calle_salida_names" value ="{{selected_calle_cruza_salida}}"/>
                    {% else %}
                        <input name = "calle_cruza_salida" type="text" list="calle_salida_names" />
                    {% endif %}
                    <datalist id="calle_salida_names">
                        {% for name in calle_salida_names %}
                        <option value="{{name}}">{{name}}</option>
                        {% endfor %}
                    </datalist>
                {% endif %}
            </div>

            <div class = 'option'>
                {% if selected_calle_llegada %}
                    <label for="input">Seleccione número de portal o calle que cruza a calle de llegada:</label>
                    {% if selected_calle_cruza_llegada %}
                        <input name = "calle_cruza_llegada" type="text" list="calle_llegada_names" value = "{{selected_calle_cruza_llegada}}"/>
                    {% else %}
                        <input name = "calle_cruza_llegada" type="text" list="calle_llegada_names" />
                    {% endif %}
                    <datalist id="calle_llegada_names">
                        {% for name in calle_llegada_names %}
                        <option value="{{name}}">{{name}}</option>
                        {% endfor %}
                    </datalist>
                {% endif %}
            </div>
            <br>
        </form>

        {% if alert_message %}
            <div class="alert">
                <p>{{alert_message}}</p>
            </div>
        {% endif %}


        {{map|safe}}
        <script>{{script|safe}}</script>
        {% if direcciones_d|length > 0 %}
            <div class='direcciones distancias'>

                <p class='title'><span class = "green"></span><strong>Trayecto de menor distancia</strong></p>
                <div class='directions'>
                    {% for direcc in direcciones_d %}
                        <p>{{ direcc|safe }}</p>
                    {% endfor %}
                </div>
                                        
            </div>
            <div class='direcciones velocidades'>
                <p class='title'><span class = "blue"></span><strong>Trayecto de menor duración</strong></p>
                <div class='directions'>
                    {% for direcc in direcciones_v %}
                        <p>{{ direcc|safe }}</p>
                    {% endfor %}
                </div>
                                        
            </div>
            <div class = 'leyenda'>
                <p><span class = "green"></span><strong>Trayecto de menor distancia</strong></p>
                <p><span class = "blue"></span><strong>Trayecto de menor duración</strong></p>
            </div>
        {% endif %}
    </body>
</html>
"""
