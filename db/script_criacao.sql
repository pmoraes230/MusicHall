-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema musicHall
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema musicHall
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `musicHall` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema musichall
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema musichall
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `musichall` DEFAULT CHARACTER SET utf8mb3 ;
USE `musicHall` ;

-- -----------------------------------------------------
-- Table `musicHall`.`Perfil`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musicHall`.`Perfil` (
  `ID_Perfil` INT NOT NULL AUTO_INCREMENT,
  `Nome_Perfil` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID_Perfil`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musicHall`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musicHall`.`Usuario` (
  `ID_Usuario` INT NOT NULL AUTO_INCREMENT,
  `Nome_Usuario` VARCHAR(45) NOT NULL,
  `Email_Usuario` VARCHAR(80) NOT NULL,
  `CPF_Usuario` VARCHAR(14) NOT NULL,
  `Senha_Usuario` VARCHAR(130) NOT NULL,
  `Perfil_ID` INT NOT NULL,
  PRIMARY KEY (`ID_Usuario`),
  UNIQUE INDEX `Email_Usuario_UNIQUE` (`Email_Usuario` ASC) VISIBLE,
  UNIQUE INDEX `CPF_Usuario_UNIQUE` (`CPF_Usuario` ASC) VISIBLE,
  UNIQUE INDEX `Senha_Usuario_UNIQUE` (`Senha_Usuario` ASC) VISIBLE,
  INDEX `fk_Usuario_Perfil_idx` (`Perfil_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Usuario_Perfil`
    FOREIGN KEY (`Perfil_ID`)
    REFERENCES `musicHall`.`Perfil` (`ID_Perfil`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musicHall`.`Evento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musicHall`.`Evento` (
  `ID_Evento` INT NOT NULL AUTO_INCREMENT,
  `Nome_Evento` VARCHAR(45) NOT NULL,
  `LimitePessoas_Evento` INT NOT NULL,
  `Data_Evento` DATE NOT NULL,
  `Horario_Evento` TIME NOT NULL,
  `Descricao_Evento` TEXT(500) NOT NULL,
  `Imagem_Evento` VARCHAR(45) NULL,
  `Usuario_ID_Usuario` INT NOT NULL,
  PRIMARY KEY (`ID_Evento`),
  INDEX `fk_Evento_Usuario1_idx` (`Usuario_ID_Usuario` ASC) VISIBLE,
  CONSTRAINT `fk_Evento_Usuario1`
    FOREIGN KEY (`Usuario_ID_Usuario`)
    REFERENCES `musicHall`.`Usuario` (`ID_Usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musicHall`.`Setor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musicHall`.`Setor` (
  `ID_Setor` INT NOT NULL AUTO_INCREMENT,
  `Nome_Setor` VARCHAR(45) NOT NULL,
  `LImite_Setor` INT NOT NULL,
  `Preco_Setor` DECIMAL(10,2) NOT NULL,
  `Evento_ID_Evento` INT NOT NULL,
  PRIMARY KEY (`ID_Setor`),
  INDEX `fk_Setor_Evento1_idx` (`Evento_ID_Evento` ASC) VISIBLE,
  CONSTRAINT `fk_Setor_Evento1`
    FOREIGN KEY (`Evento_ID_Evento`)
    REFERENCES `musicHall`.`Evento` (`ID_Evento`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musicHall`.`Cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musicHall`.`Cliente` (
  `ID_Cliente` INT NOT NULL AUTO_INCREMENT,
  `Nome_Cliente` VARCHAR(45) NOT NULL,
  `CPF_Cliente` VARCHAR(14) NOT NULL,
  `Email_Cliente` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`ID_Cliente`),
  UNIQUE INDEX `CPF_Cliente_UNIQUE` (`CPF_Cliente` ASC) VISIBLE,
  UNIQUE INDEX `Email_Cliente_UNIQUE` (`Email_Cliente` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `musicHall`.`Ingresso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musicHall`.`Ingresso` (
  `Cliente_ID` INT NOT NULL,
  `Evento_ID` INT NOT NULL,
  `Setor_ID` INT NOT NULL,
  `ID_Ingresso` VARCHAR(45) NOT NULL,
  `Data_Emissao_Ingresso` DATETIME NOT NULL,
  `Status_Ingresso` ENUM("emitido", "validado", "cancelado") NULL DEFAULT 'emitido',
  INDEX `fk_Cliente_has_Evento_Evento1_idx` (`Evento_ID` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Evento_Cliente1_idx` (`Cliente_ID` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Evento_Setor1_idx` (`Setor_ID` ASC) VISIBLE,
  PRIMARY KEY (`ID_Ingresso`),
  UNIQUE INDEX `ID_Ingresso_UNIQUE` (`ID_Ingresso` ASC) VISIBLE,
  CONSTRAINT `fk_Cliente_has_Evento_Cliente1`
    FOREIGN KEY (`Cliente_ID`)
    REFERENCES `musicHall`.`Cliente` (`ID_Cliente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Cliente_has_Evento_Evento1`
    FOREIGN KEY (`Evento_ID`)
    REFERENCES `musicHall`.`Evento` (`ID_Evento`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Cliente_has_Evento_Setor1`
    FOREIGN KEY (`Setor_ID`)
    REFERENCES `musicHall`.`Setor` (`ID_Setor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

USE `musichall` ;

-- -----------------------------------------------------
-- Table `musichall`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musichall`.`cliente` (
  `ID_Cliente` INT NOT NULL AUTO_INCREMENT,
  `Nome_Cliente` VARCHAR(45) NOT NULL,
  `CPF_Cliente` VARCHAR(14) NOT NULL,
  `Email_Cliente` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`ID_Cliente`),
  UNIQUE INDEX `CPF_Cliente_UNIQUE` (`CPF_Cliente` ASC) VISIBLE,
  UNIQUE INDEX `Email_Cliente_UNIQUE` (`Email_Cliente` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `musichall`.`perfil`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musichall`.`perfil` (
  `ID_Perfil` INT NOT NULL AUTO_INCREMENT,
  `Nome_Perfil` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID_Perfil`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `musichall`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musichall`.`usuario` (
  `ID_Usuario` INT NOT NULL AUTO_INCREMENT,
  `Nome_Usuario` VARCHAR(45) NOT NULL,
  `Email_Usuario` VARCHAR(80) NOT NULL,
  `CPF_Usuario` VARCHAR(14) NOT NULL,
  `Senha_Usuario` VARCHAR(45) NOT NULL,
  `Perfil_ID` INT NOT NULL,
  PRIMARY KEY (`ID_Usuario`),
  UNIQUE INDEX `Email_Usuario_UNIQUE` (`Email_Usuario` ASC) VISIBLE,
  UNIQUE INDEX `CPF_Usuario_UNIQUE` (`CPF_Usuario` ASC) VISIBLE,
  UNIQUE INDEX `Senha_Usuario_UNIQUE` (`Senha_Usuario` ASC) VISIBLE,
  INDEX `fk_Usuario_Perfil_idx` (`Perfil_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Usuario_Perfil`
    FOREIGN KEY (`Perfil_ID`)
    REFERENCES `musichall`.`perfil` (`ID_Perfil`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `musichall`.`evento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musichall`.`evento` (
  `ID_Evento` INT NOT NULL AUTO_INCREMENT,
  `Nome_Evento` VARCHAR(45) NOT NULL,
  `LimitePessoas_Evento` INT NOT NULL,
  `Data_Evento` DATE NOT NULL,
  `Horario_Evento` TIME NOT NULL,
  `Descricao_Evento` TEXT NOT NULL,
  `Imagem_Evento` VARCHAR(45) NULL DEFAULT NULL,
  `Usuario_ID_Usuario` INT NOT NULL,
  PRIMARY KEY (`ID_Evento`),
  INDEX `fk_Evento_Usuario1_idx` (`Usuario_ID_Usuario` ASC) VISIBLE,
  CONSTRAINT `fk_Evento_Usuario1`
    FOREIGN KEY (`Usuario_ID_Usuario`)
    REFERENCES `musichall`.`usuario` (`ID_Usuario`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `musichall`.`setor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musichall`.`setor` (
  `ID_Setor` INT NOT NULL AUTO_INCREMENT,
  `Nome_Setor` VARCHAR(45) NOT NULL,
  `LImite_Setor` INT NOT NULL,
  `Preco_Setor` DECIMAL(10,2) NOT NULL,
  `Evento_ID_Evento` INT NOT NULL,
  PRIMARY KEY (`ID_Setor`),
  INDEX `fk_Setor_Evento1_idx` (`Evento_ID_Evento` ASC) VISIBLE,
  CONSTRAINT `fk_Setor_Evento1`
    FOREIGN KEY (`Evento_ID_Evento`)
    REFERENCES `musichall`.`evento` (`ID_Evento`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `musichall`.`ingresso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `musichall`.`ingresso` (
  `Cliente_ID` INT NOT NULL,
  `Evento_ID` INT NOT NULL,
  `Setor_ID` INT NOT NULL,
  `ID_Ingresso` VARCHAR(45) NOT NULL,
  `Data_Emissao_Ingresso` DATETIME NOT NULL,
  `Status_Ingresso` ENUM('emitido', 'validado', 'cancelado') NULL DEFAULT 'emitido',
  PRIMARY KEY (`ID_Ingresso`),
  UNIQUE INDEX `ID_Ingresso_UNIQUE` (`ID_Ingresso` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Evento_Evento1_idx` (`Evento_ID` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Evento_Cliente1_idx` (`Cliente_ID` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Evento_Setor1_idx` (`Setor_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Cliente_has_Evento_Cliente1`
    FOREIGN KEY (`Cliente_ID`)
    REFERENCES `musichall`.`cliente` (`ID_Cliente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Cliente_has_Evento_Evento1`
    FOREIGN KEY (`Evento_ID`)
    REFERENCES `musichall`.`evento` (`ID_Evento`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Cliente_has_Evento_Setor1`
    FOREIGN KEY (`Setor_ID`)
    REFERENCES `musichall`.`setor` (`ID_Setor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
