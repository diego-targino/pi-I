import { Link } from "react-router-dom";
import iconSeta from "../assets/images/icon-seta.png";

export default function CardPlanta({ id, imagem, nome, descricao, rotaLink }) {
  return (
    <Link to={rotaLink} style={{ textDecoration: 'none', color: 'inherit' }}>
      <div className="box-plant">
        <div className="image-plant">
          <img src={imagem} alt={nome} />
        </div>

        <div className="info-plant">
          <div className="title-plant">
            <h3>{nome}</h3>
          </div>

          <div className="description-plant">
            <p>{descricao}</p>
          </div>
          
          <div className="button-seta"> 
            <img src={iconSeta} alt="Avançar" />
            <p>Saiba mais</p>
          </div>
        </div>
      </div>
    </Link>
  );
}