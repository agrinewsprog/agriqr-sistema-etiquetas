    def actualizar_indicadores_pulseras(self):
        """Actualiza los indicadores visuales de pulseras y mochilas según los datos actuales."""
        if not hasattr(self, 'datos_actual') or not self.datos_actual:
            # Ocultar indicadores activos si no hay datos
            self.indicador_activo.pack_forget()
            self.indicador_mochila_activo.pack_forget()
            return
        
        # Obtener datos
        tipo_entrada = self.datos_actual.get('Entrada') or self.datos_actual.get('entrada', '')
        pirata = self.datos_actual.get('pirata', 0)
        
        if self.modo_csv:
            evento_id = self.datos_actual.get('Evento', '0')
            nombre_evento = self.obtener_nombre_evento_csv(evento_id)
        else:
            evento_id = self.datos_actual.get('Evento', 0)
            nombre_evento = self.obtener_nombre_evento_mysql(evento_id)
        
        # Normalizar para comparación
        evento_lower = nombre_evento.lower() if nombre_evento else ''
        tipo_lower = tipo_entrada.lower() if tipo_entrada else ''
        
        # Convertir pirata a entero de forma segura
        try:
            pirata_valor = int(str(pirata).strip()) if pirata is not None and str(pirata).strip() != '' else 0
        except (ValueError, TypeError):
            pirata_valor = 0
        
        # Debug
        print("=" * 50)
        print(f"👤 {self.datos_actual.get('Nombrecompleto', 'N/A')}")
        print(f"📅 Evento: {nombre_evento}")
        print(f"🎫 Tipo: {tipo_entrada}")
        print(f"🏴‍☠️ Pirata: {pirata_valor}")
        
        # Resetear TODOS los indicadores
        self.pulsera_naranja.configure(relief='raised', borderwidth=2)
        self.pulsera_azul.configure(relief='raised', borderwidth=2)
        self.pulsera_negra.configure(relief='raised', borderwidth=2)
        self.indicador_activo.pack_forget()
        self.mochila_si.configure(relief='raised', borderwidth=2)
        self.mochila_no.configure(relief='raised', borderwidth=2)
        self.indicador_mochila_activo.pack_forget()
        
        # === 3 PULSERAS EXACTAS ===
        
        # 1. NEGRA → Cualquier EXPO
        if 'expo' in tipo_lower:
            print("⚫ PULSERA NEGRA (EXPO)")
            self.pulsera_negra.configure(relief='solid', borderwidth=4)
            self.indicador_activo.configure(text="👆 PULSERA NEGRA", bg='#2C2C2C', fg='white')
            self.indicador_activo.pack(after=self.pulsera_negra, pady=(2, 0))
            
            # EXPO = NO MOCHILA
            self.mochila_no.configure(relief='solid', borderwidth=4)
            self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA", bg='#2C2C2C', fg='white')
            self.indicador_mochila_activo.pack(after=self.mochila_no, pady=(2, 0))
            
        # 2. NARANJA → LPN Congress
        elif 'lpn' in evento_lower and ('congress' in tipo_lower or 'congreso' in tipo_lower):
            print("🟠 PULSERA NARANJA (LPN CONGRESS)")
            self.pulsera_naranja.configure(relief='solid', borderwidth=4)
            self.indicador_activo.configure(text="👆 PULSERA NARANJA", bg='#fd7e14', fg='white')
            self.indicador_activo.pack(after=self.pulsera_naranja, pady=(2, 0))
            
            # Mochila según pirata
            if pirata_valor == 0:
                self.mochila_si.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 ENTREGAR MOCHILA", bg='#28a745', fg='white')
                self.indicador_mochila_activo.pack(after=self.mochila_si, pady=(2, 0))
            else:
                self.mochila_no.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA", bg='#dc3545', fg='white')
                self.indicador_mochila_activo.pack(after=self.mochila_no, pady=(2, 0))
                
        # 3. AZUL → PorciForum Latam Congress
        elif ('porciforum' in evento_lower or 'porci forum' in evento_lower) and ('congress' in tipo_lower or 'congreso' in tipo_lower):
            print("🔵 PULSERA AZUL (PORCIFORUM CONGRESS)")
            self.pulsera_azul.configure(relief='solid', borderwidth=4)
            self.indicador_activo.configure(text="👆 PULSERA AZUL", bg='#007bff', fg='white')
            self.indicador_activo.pack(after=self.pulsera_azul, pady=(2, 0))
            
            # Mochila según pirata
            if pirata_valor == 0:
                self.mochila_si.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 ENTREGAR MOCHILA", bg='#28a745', fg='white')
                self.indicador_mochila_activo.pack(after=self.mochila_si, pady=(2, 0))
            else:
                self.mochila_no.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA", bg='#dc3545', fg='white')
                self.indicador_mochila_activo.pack(after=self.mochila_no, pady=(2, 0))
                
        else:
            print("⚠️ CASO NO RECONOCIDO")
            # Default: mochila según pirata
            if pirata_valor == 0:
                self.mochila_si.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 ENTREGAR MOCHILA (DEFAULT)", bg='#ffc107', fg='black')
                self.indicador_mochila_activo.pack(after=self.mochila_si, pady=(2, 0))
            else:
                self.mochila_no.configure(relief='solid', borderwidth=4)
                self.indicador_mochila_activo.configure(text="👆 NO ENTREGAR MOCHILA (DEFAULT)", bg='#ffc107', fg='black')
                self.indicador_mochila_activo.pack(after=self.mochila_no, pady=(2, 0))
        
        print("=" * 50)