CREATE TABLE pedidos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre_cliente VARCHAR(255) NOT NULL,
  direccion_envio VARCHAR(255) NOT NULL,
  productos TEXT NOT NULL,
  estado VARCHAR(255) NOT NULL DEFAULT 'pendiente'
);

INSERT INTO pedidos (nombre_cliente, direccion_envio, productos, estado) VALUES
('Ivan', 'C/Cimadevilla', 'Cafetera','pendiente');
