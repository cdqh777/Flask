-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-10-2025 a las 04:24:59
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ventas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `email`) VALUES
(1, 'Ana Pérez', 'ana.perez@gmail.com'),
(2, 'Luis Gómez', 'luis.gomez@hotmail.com'),
(3, 'María López', 'maria.lopez@yahoo.com'),
(4, 'Esteban Dido', 'esteban.dido@gmail.com'),
(5, 'Carlos Mendoza', 'c.mendoza@gmail.com'),
(6, 'Sofía Ramírez', 'sofia.ramirez@hotmail.com'),
(7, 'Pedro Castillo', 'pedro.castillo@yahoo.com'),
(8, 'Lucía Fernández', 'lucia.fernandez@gmail.com'),
(9, 'Javier Morales', 'javier.morales@hotmail.com'),
(10, 'Andrea Vargas', 'andrea.vargas@gmail.com'),
(11, 'Fernando López', 'fernando.lopez@yahoo.com'),
(12, 'Patricia Gutiérrez', 'patricia.gutierrez@gmail.com'),
(13, 'Raúl Ortega', 'raul.ortega@hotmail.com'),
(14, 'Gabriela Suárez', 'gabriela.suarez@gmail.com'),
(15, 'Miguel Torres', 'miguel.torres@gmail.com'),
(16, 'Natalia Rojas', 'natalia.rojas@hotmail.com'),
(17, 'Héctor Silva', 'hector.silva@yahoo.com'),
(18, 'Verónica Castro', 'veronica.castro@gmail.com'),
(19, 'Esteban Reyes', 'esteban.reyes@hotmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `id_compra` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_tienda` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `compras`
--

INSERT INTO `compras` (`id_compra`, `fecha`, `monto`, `id_cliente`, `id_tienda`) VALUES
(1, '2025-09-01', 150.50, 1, 1),
(2, '2025-09-02', 300.00, 2, 2),
(3, '2025-09-03', 75.25, 3, 3),
(4, '2025-09-11', 250.00, 2, 3),
(5, '2025-09-11', 100.00, 2, 3),
(6, '2025-09-01', 120.50, 1, 3),
(7, '2025-09-01', 350.00, 2, 5),
(8, '2025-09-02', 89.90, 3, 1),
(9, '2025-09-02', 210.00, 4, 2),
(10, '2025-09-03', 480.75, 5, 4),
(11, '2025-09-03', 135.00, 6, 5),
(12, '2025-09-04', 299.99, 7, 6),
(13, '2025-09-04', 60.00, 8, 7),
(14, '2025-09-05', 180.25, 9, 8),
(15, '2025-09-05', 512.00, 10, 9),
(16, '2025-09-06', 75.50, 11, 10),
(17, '2025-09-06', 220.00, 12, 1),
(18, '2025-09-07', 99.90, 13, 2),
(19, '2025-09-07', 150.00, 14, 3),
(20, '2025-09-08', 330.80, 15, 4),
(21, '2025-09-08', 440.00, 2, 6),
(22, '2025-09-09', 125.25, 5, 7),
(23, '2025-09-09', 300.00, 9, 8),
(24, '2025-09-10', 510.10, 12, 10),
(25, '2025-09-10', 95.00, 7, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tiendas`
--

CREATE TABLE `tiendas` (
  `id_tienda` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tiendas`
--

INSERT INTO `tiendas` (`id_tienda`, `nombre`, `direccion`) VALUES
(1, 'Tienda Central', 'Av. Siempre Viva 123'),
(2, 'Sucursal Norte', 'Calle Libertad 45'),
(3, 'Sucursal Sur', 'Av. América 789'),
(4, 'Sucursal Este', 'Av. Bolívar 120'),
(5, 'Sucursal Oeste', 'Calle Sucre 45'),
(6, 'Sucursal Norte', 'Av. América 789'),
(7, 'Sucursal Sur', 'Av. Villazón 234'),
(8, 'Tienda Central', 'Av. Siempre Viva 123'),
(9, 'Sucursal Altos', 'Calle Ayacucho 67'),
(10, 'Sucursal Valle', 'Av. Los Pinos 345'),
(11, 'Sucursal Río', 'Calle Colón 88'),
(12, 'Sucursal Lago', 'Av. Mariscal 456'),
(13, 'Sucursal Montaña', 'Calle Murillo 210');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `rol` enum('admin','operator') NOT NULL DEFAULT 'operator',
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `password_hash`, `nombre`, `rol`, `activo`) VALUES
(1, 'admin', 'scrypt:32768:8:1$k3gVHZ7f02dLn45D$f0e2b623339f50c6035a2b5056058dedf85d657729835c81e8d83fc1ca142a3d8b18334fe62aa85671839e47720e46888285c679ada74d947870631d0d71028e', 'administrador', 'admin', 1),
(2, 'oper1', 'scrypt:32768:8:1$5NPBQA4TQvle1yLb$3e56b92a8c888a4e1e928015e28c49f16ecdf1689145baeaef7a130852ad4d49d1d8dee4e1141bb09d7fdeb3176d25cb084248b21ba7bdd787ed4959f71b7356', 'operador 1', 'operator', 1),
(3, 'oper2', 'scrypt:32768:8:1$f1TajDiOypAO0joD$07e0636e268c0616be054ae634be398e9c584f5624441bed9a3fd1f7539ecf8611604dd14f2d7280270ef67d6b866f03473760c4291b36f695b4cd24ae39fdeb', 'operador 2', 'operator', 1),
(4, 'invitado', 'scrypt:32768:8:1$ODmDEdIphrnOFA7L$c130e64246c68f88c8b9e71d0e6a618c7c5033f243c43ca04b8f9b5892f4382d035cf6f02db847742630a53535e31ae8bfc88e2d945e77eb9587218f6b0b1282', 'invitado', 'operator', 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_tienda` (`id_tienda`);

--
-- Indices de la tabla `tiendas`
--
ALTER TABLE `tiendas`
  ADD PRIMARY KEY (`id_tienda`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `id_compra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `tiendas`
--
ALTER TABLE `tiendas`
  MODIFY `id_tienda` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `compras`
--
ALTER TABLE `compras`
  ADD CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`id_tienda`) REFERENCES `tiendas` (`id_tienda`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
