from offers_service import OffersService

def mostrar_produtos_hotspot(hotspot_id='hs001'):
    try:
        svc = OffersService()
        produtos = svc.get_hotspot_products(hotspot_id)
        
        print(f"\nPRODUTOS NO HOTSPOT {hotspot_id}")
        print("=" * 60)
        
        for prod in produtos:
            status = " ATIVO" if prod.get('is_active', False) else " INATIVO"
            print(f"\n {prod.get('nomeProduto', 'Nome não disponível')} ({status})")
            print(f" Preço: R${prod.get('preco', 0):.2f}")
            print(f" Categoria: {prod.get('categoria', 'Não especificada')}")
            print(f" Validade: {prod.get('dataInicio', '')} a {prod.get('dataFim', '')}")
            print(f" Dias restantes: {prod.get('days_remaining', 0)}")
            
        print(f"\nTotal de produtos encontrados: {len(produtos)}")
        
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    mostrar_produtos_hotspot('hs002') 