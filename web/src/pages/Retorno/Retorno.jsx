import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import MenuLateral from "../MenuLateral/MenuLateral";

import logo from "../../assets/images/Logo-AnalisaAI.png";
import iconMenu from "../../assets/images/icon-menu.png";
import iconPerson from "../../assets/images/icon-person.png";
import fotoTeste from "../../assets/images/fototeste.jpeg";

import "../Home/Home.css";
import "./Retorno.css"; 
import "../Resultado/Resultado.css";
import useAnalysisStore from "../../stores/analysisStore";

export default function Retorno() {
  const [menuAberto, setMenuAberto] = useState(false);
  const navigate = useNavigate();
  const location = useLocation(); 
  const { searchRequestId, analysis } = useAnalysisStore();
  const imagemEnviada = location.state?.imagemUrl || fotoTeste;

  if (!analysis || analysis.length === 0) {
    return (
      <div id="resultado-container">
        <header>
          <div id="cabecalho">
            <img
              id="icon-menu"
              src={iconMenu}
              alt="Menu"
              onClick={() => setMenuAberto(true)}
            />
            <img
              id="logo"
              src={logo}
              alt="Logo"
              onClick={() => navigate("/home")}
              style={{ cursor: "pointer" }}
            />
            <img id="icon-person" src={iconPerson} alt="Perfil" />
          </div>
        </header>

        <main id="detalhes-planta" className="erro-analise">
          <h2>Erro ao analisar a sua foto</h2>
          <button className="voltar" onClick={() => navigate("/home")}>
            Voltar para o início
          </button>
        </main>

        <MenuLateral menuAberto={menuAberto} setMenuAberto={setMenuAberto} />
      </div>
    );
  }

  return (
    <div id="resultado-container">
      <header>
        <div id="cabecalho">
          <img
            id="icon-menu"
            src={iconMenu}
            alt="Menu"
            onClick={() => setMenuAberto(true)}
          />
          <img
            id="logo"
            src={logo}
            alt="Logo"
            onClick={() => navigate("/home")}
            style={{ cursor: "pointer" }}
          />
          <img id="icon-person" src={iconPerson} alt="Perfil" />
        </div>
      </header>

      <main id="detalhes-planta">
        <div className="top-navigation">
          <button className="voltar" onClick={() => navigate("/home")}>
            ⬅ Analisar outra planta
          </button>
          <h2>Resultado da Análise</h2>
        </div>

        <div className="container-description">
          <div className="resultado-imagem">
            <img src={imagemEnviada} alt="Foto da planta analisada" />
          </div>

          <div className="info-box box1">
            <div className="info-group">
              <h3>Nome popular</h3>
              <p>{analysis[0].CommonName}</p> 
            </div>

            <div className="info-group">
              <h3>Descrição</h3>
              <p>{analysis[0].Description}</p> {/* Aguardando Backend */}
            </div>

            <div className="info-group">
              <h3>Espécies suscetíveis à intoxicação</h3>
              {analysis[0]?.SusceptibleAnimalSpecies?.map((especie, index) => (
                <p key={index}>{especie}</p>
              ))} 
            </div>
          </div>

          <div className="info-box box2">
            <div className="info-group">
              <h3>Riscos</h3>
              <p>{analysis[0].HumanRisks}</p> 
            </div>

            <div className="info-group">
              <h3>Sintomas</h3>
              {analysis[0]?.CommonSymptoms?.map((especie, index) => (
                <p key={index}>{especie}</p>
              ))}
            </div>

            <div className="info-group">
              <h3>Ações recomendadas</h3>
              {analysis[0]?.RecommendedActions?.map((especie, index) => (
                <p key={index}>{especie}</p>
              ))}
            </div>
          </div>
        </div>
      </main>

      <MenuLateral menuAberto={menuAberto} setMenuAberto={setMenuAberto} />
    </div>
  );
}