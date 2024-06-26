from resources.modules.actuaciones import ActuacionesModule
from resources.modules.causa import CausasModule
from resources.modules.movimiento import MovimientosModule
from resources.modules.persona import PersonasModule


async def save_info(process_links_results, person_id):
    try:
        created_persona = await PersonasModule.get_personas(identificacion=person_id)

        if created_persona:
            created_persona = created_persona[0]
        else:
            created_persona = await PersonasModule.create(**{"identificacion": person_id})
        for process_links_result in process_links_results:
            process_links_details = {
                **process_links_result,
                **process_links_result.get('process_link_info', {}),
                "persona_id": created_persona.get('id')
            }
            created_causa = await CausasModule.create(**process_links_details)

            for movimiento in process_links_details.get('movimientos', []):
                movimiento_details = {
                    **movimiento,
                    **movimiento.get('juditial_actions_info', {}),
                    'causa_id': created_causa.get('id')
                }
                created_movimiento = await MovimientosModule.create(**movimiento_details)

                for actuacion in movimiento_details.get('actuaciones', []):
                    actuacion['movimiento_id'] = created_movimiento.get('id')
                    await ActuacionesModule.create(**actuacion)

    except Exception as e:
        return None