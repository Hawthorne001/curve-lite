from scripts.tests.post_deploy.utils import check_contracts, get_contract
from settings.config import RollupType


def test_registries_deployment(whole_deployment: dict, chain_settings):
    contracts = {
        k: {**v, "contract": get_contract(v["contract_github_url"], v["address"])}
        for k, v in whole_deployment["registries"].items()
    }
    check_contracts(contracts)

    # <-------------------------- Address Provider -------------------------->
    address_provider = contracts["address_provider"]["contract"]
    fee_receiver = chain_settings.dao.vault
    if chain_settings.rollup_type != RollupType.not_rollup:
        gov_contracts = whole_deployment.get("governance")
        assert gov_contracts
        assert gov_contracts.get("vault")
        fee_receiver = gov_contracts["vault"]["address"]

    assert address_provider.get_address(2) == whole_deployment["helpers"]["router"]["address"]
    assert address_provider.get_address(4) == fee_receiver
    assert address_provider.get_address(7) == whole_deployment["registries"]["metaregistry"]["address"]
    assert address_provider.get_address(11) == whole_deployment["amm"]["tricryptoswap"]["factory"]["address"]
    assert address_provider.get_address(12) == whole_deployment["amm"]["stableswap"]["factory"]["address"]
    assert address_provider.get_address(13) == whole_deployment["amm"]["twocryptoswap"]["factory"]["address"]
    assert address_provider.get_address(18) == whole_deployment["helpers"]["rate_provider"]["address"]
    assert address_provider.get_address(26) == whole_deployment["helpers"]["deposit_and_stake_zap"]["address"]
    assert address_provider.get_address(27) == whole_deployment["helpers"]["stable_swap_meta_zap"]["address"]

    # <-------------------------- Metaregistry -------------------------->
    meta_registry = contracts["metaregistry"]["contract"]

    assert meta_registry.get_registry(0) == contracts["metaregistry"]["registry_handlers"]["stableswap"]["address"]
    assert meta_registry.get_registry(1) == contracts["metaregistry"]["registry_handlers"]["tricryptoswap"]["address"]
    assert meta_registry.get_registry(2) == contracts["metaregistry"]["registry_handlers"]["twocryptoswap"]["address"]
